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

# Remove incomplete runs
rm -rf *l3-08M*.csmb-1000
rm -rf *l3-08M*.csmb-0010
rm -rf *l3-08M*.csmb-0001

rm -rf *l3-16M*.csmb-1000
rm -rf *l3-16M*.csmb-0010
rm -rf *l3-16M*.csmb-0001

du -sh .
ls * | wc -l
