du -sh .
ls * | wc -l

# Remove old runs
rm -rf _figures
rm -rf *drrip-4*
rm -rf *prism-*
rm -rf *pipp-s*
rm -rf *pipp-min16*

# Fix bad csmb values
rename -v 100 0100 *-100
rm -rf *-100

du -sh .
ls * | wc -l
