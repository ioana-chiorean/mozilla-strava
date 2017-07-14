export STRAVA_PUBLIC_AUTH=`cat ~/.strava-token`
python get_weekly.py
git commit -m "daily updates" -a
git push
