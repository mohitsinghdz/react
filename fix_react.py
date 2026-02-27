#!/usr/bin/env python3
import re

# Read the file
with open('/home/engine/project/packages/react-reconciler/src/ReactFiberWorkLoop.js', 'r') as f:
    content = f.read()

# Define the replacement for performWorkOnRoot (first occurrence)
old_perform_work = """export function performWorkOnRoot(
  root: FiberRoot,
  lanes: Lanes,
  forceSync: boolean,
): void {
  if ((executionContext & (RenderContext | CommitContext)) !== NoContext) {
    throw new Error('Should not already be working.');
  }

  if (enableProfilerTimer && enableComponentPerformanceTrack) {
    if (workInProgressRootRenderLanes !== NoLanes && workInProgress !== null) {
      const yieldedFiber = workInProgress;
      // We've returned from yielding to the event loop. Let's log the time it took.
      const yieldEndTime = now();
      switch (yieldReason) {"""

new_perform_work = """export function performWorkOnRoot(
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
  }

  if (enableProfilerTimer && enableComponentPerformanceTrack) {
    if (workInProgressRootRenderLanes !== NoLanes && workInProgress !== null) {
      const yieldedFiber = workInProgress;
      // We've returned from yielding to the event loop. Let's log the time it took.
      const yieldEndTime = now();
      switch (yieldReason) {"""

# Find and replace only the first occurrence (performWorkOnRoot)
# We'll use a more specific pattern to target the right location
pattern1 = r"(export function performWorkOnRoot\(\s*root: FiberRoot,\s*lanes: Lanes,\s*forceSync: boolean,\s*\): void \{)\s+(if \(\(executionContext & \(RenderContext \| CommitContext\)\) !== NoContext\) \{\s+throw new Error\('Should not already be working\.'\);\s+\})"

replacement1 = r"""\1
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
  }"""

content = re.sub(pattern1, replacement1, content, count=1)

# Define the replacement for completeRoot (second occurrence)
pattern2 = r"(do \{\s+// `flushPassiveEffects` will call `flushSyncUpdateQueue` at the end.*?)\s+(if \(\(executionContext & \(RenderContext \| CommitContext\)\) !== NoContext\) \{\s+throw new Error\('Should not already be working\.'\);\s+\})"

replacement2 = r"""\1

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
  }"""

content = re.sub(pattern2, replacement2, content, count=1)

# Write the file back
with open('/home/engine/project/packages/react-reconciler/src/ReactFiberWorkLoop.js', 'w') as f:
    f.write(content)

print("Successfully updated ReactFiberWorkLoop.js")
