# Forensic Analysis Plan — Remaining Images

## Priority Order

1. **nz-mem0** (7.9 GB) — Priority 1
   - Largest image, likely complex dependencies
   - May have similar missing dependency issues
   
2. **nz-intent-adapter** (184 MB) — Priority 2
   - Smaller, faster to analyze
   
3. **nz-stack-core** (171 MB) — Priority 3
   - Core component, verify stability
   
4. **genesis-core** (N/A) — Special Case
   - Unknown origin
   - May need manual source investigation

## Forensic Method

For each image:

1. Pull from GHCR
2. Extract source code
3. Check for:
   - Missing dependencies (like lightrag issue)
   - Broken imports
   - Configuration issues
   - Dead code
4. Test basic import functionality
5. Document findings
6. Create remediation plan if needed

## Questions for Each Image

- Does the image start without errors?
- Are all imports resolvable?
- Are config files valid?
- Is the entrypoint functional?
- Are there obvious bugs?

## Special Notes

### genesis-core
- NOT in git history
- Unknown source repository
- May require manual investigation
- Consider: Is this a monorepo component?
