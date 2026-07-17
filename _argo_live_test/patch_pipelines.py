#!/usr/bin/env python3
"""Patch all pipeline YAMLs for Argo compatibility:
1. generateName: underscores → hyphens, ensure ends with alphanumeric
2. volumes emptyDir → volumeClaimTemplates (shared PVC)
3. Add default serviceAccount if missing
"""
import os, re, glob

BASE = "/Users/abubakarialidu/Downloads/custom_pipelines"

for pipe_dir in sorted(glob.glob(os.path.join(BASE, "*/"))):
    dirname = os.path.basename(pipe_dir.rstrip("/"))
    if not dirname[0].isdigit():
        continue

    yaml_path = os.path.join(pipe_dir, "pipeline.yaml")
    if not os.path.exists(yaml_path):
        continue

    with open(yaml_path) as f:
        content = f.read()

    original = content

    # Fix 1: generateName - replace underscores with hyphens, ensure ends with alphanumeric
    content = re.sub(
        r'(generateName:\s*)(\S+)',
        lambda m: m.group(1) + m.group(2).replace('_', '-').rstrip('-'),
        content
    )
    # If the generateName now ends with non-alphanumeric, append 'wf'
    content = re.sub(
        r'(generateName:\s*)(\S*[^a-z0-9])(\s*)$',
        r'\1\2wf\3',
        content
    )

    # Fix 2: Replace emptyDir volume with volumeClaimTemplates
    if 'emptyDir: {}' in content or 'emptyDir:{}' in content:
        # Remove old volumes block
        content = re.sub(
            r'\n\s*volumes:\s*\n\s*- name: pipeline-output\s*\n\s*emptyDir:\s*\{\}\s*',
            '',
            content
        )
        # Add volumeClaimTemplates after podGC
        vct = """
  volumeClaimTemplates:
  - metadata:
      name: pipeline-output
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: local-path
      resources:
        requests:
          storage: 1Gi
"""
        if 'volumeClaimTemplates' not in content:
            content = content.replace(
                'podGC:\n    strategy: OnWorkflowCompletion\n',
                'podGC:\n    strategy: OnWorkflowCompletion\n' + vct
            )

    # Fix 3: Add serviceAccountName if not set
    if 'serviceAccountName' not in content and 'spec:' in content:
        # Add after 'entrypoint: pipeline' line
        content = re.sub(
            r'(entrypoint:\s*pipeline\s*\n)',
            r'\1  serviceAccountName: argo-workflow\n',
            content
        )

    # Fix 4: Sanitize labels - replace spaces with hyphens, lowercase domain values
    content = re.sub(
        r'(\s+domain:\s+)(.+)',
        lambda m: m.group(1) + m.group(2).strip().replace(' ', '-').replace('_', '-'),
        content
    )
    content = re.sub(
        r'(\s+type:\s+)(.+)',
        lambda m: m.group(1) + m.group(2).strip().replace(' ', '-').replace('_', '-'),
        content
    )

    if content != original:
        with open(yaml_path, "w") as f:
            f.write(content)
        print(f"  ✓ {dirname}")
    else:
        print(f"  - {dirname} (no changes)")

print(f"\nDone. Patched pipelines in {BASE}")
