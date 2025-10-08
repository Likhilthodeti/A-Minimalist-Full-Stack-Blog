git pull origin main

# Loop from 2025-09-26 to 2025-10-07
for day in {26..30}
do
  date="2025-09-$day"
  echo "Update for $date" >> progress_log.txt
  git add progress_log.txt
  GIT_AUTHOR_DATE="${date}T12:00:00" GIT_COMMITTER_DATE="${date}T12:00:00" git commit -m "Progress update on ${date}"
done

for day in {1..7}
do
  date="2025-10-$(printf "%02d" $day)"
  echo "Update for $date" >> progress_log.txt
  git add progress_log.txt
  GIT_AUTHOR_DATE="${date}T12:00:00" GIT_COMMITTER_DATE="${date}T12:00:00" git commit -m "Progress update on ${date}"
done

# Push commits to GitHub
git push origin main