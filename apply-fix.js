const fs = require('fs');
const path = require('path');

const filePath = '/home/engine/project/packages/react-reconciler/src/ReactFiberWorkLoop.js';
const content = fs.readFileSync(filePath, 'utf8');

// Fix 1: performWorkOnRoot function (around line 1122)
const performWorkOnRootPattern = /export function performWorkOnRoot\(\s*root: FiberRoot,\s*lanes: Lanes,\s*forceSync: boolean,\s*\): void \{\s+if \(\(executionContext & \(RenderContext \| CommitContext\)\) !== NoContext\) \{\s+throw new Error\('Should not already be working\.'\);\s+\}/;

const performWorkOnRootReplacement = `export function performWorkOnRoot(
  root: FiberRoot,
  lanes: Lanes,
  forceSync: boolean,
): void {
  if ((executionContext & (RenderContext | CommitContext)) !== NoContext) {
    // Check if this is stale state from a browser interruption (breakpoint,
    // alert, debugger, tab freeze). If there's no actual work in progress,
    // we can safely reset the context and continue.
    if (
      workInProgress === null &&
      workInProgressRoot === null &&
      pendingEffectsStatus === NO_PENDING_EFFECTS
    ) {
      // The execution context is stale from a browser interruption.
      // Reset it and continue.
      executionContext = NoContext;
    } else {
      throw new Error('Should not already be working.');
    }
  }`;

let newContent = content.replace(performWorkOnRootPattern, performWorkOnRootReplacement);

// Fix 2: completeRoot function (around line 3514)
// We need to find the second occurrence after flushPendingEffects loop
const completeRootPattern = /(flushPendingEffects\(\);\s+\} while \(pendingEffectsStatus !== NO_PENDING_EFFECTS\);\s+flushRenderPhaseStrictModeWarningsInDEV\(\);\s+)(if \(\(executionContext & \(RenderContext \| CommitContext\)\) !== NoContext\) \{\s+throw new Error\('Should not already be working\.'\);\s+\})/;

const completeRootReplacement = `$1if ((executionContext & (RenderContext | CommitContext)) !== NoContext) {
    // Check if this is stale state from a browser interruption (breakpoint,
    // alert, debugger, tab freeze). If there's no actual work in progress,
    // we can safely reset the context and continue.
    if (
      workInProgress === null &&
      workInProgressRoot === null &&
      pendingEffectsStatus === NO_PENDING_EFFECTS
    ) {
      // The execution context is stale from a browser interruption.
      // Reset it and continue.
      executionContext = NoContext;
    } else {
      throw new Error('Should not already be working.');
    }
  }`;

newContent = newContent.replace(completeRootPattern, completeRootReplacement);

fs.writeFileSync(filePath, newContent, 'utf8');
console.log('Successfully applied fix to ReactFiberWorkLoop.js');
