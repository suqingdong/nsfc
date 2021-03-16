set -exo pipefail

mkdir -p log

for year in 2016 2015 2005 2004;do

for code in {A..H};do
  python3 -m nsfc.bin.main -y $year -c $code &> log/$code.$year.log
done

done
