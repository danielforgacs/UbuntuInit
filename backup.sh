dirdate=$(date +%Y-%m-%d_%H-%M-%S)
bkproot=/media/ford/PEN_128/__BACKUP__/backup_$dirdate
storagesrc=$HOME/storage/
storagedest=$bkproot/storage/

echo "====================================================="
date
echo "--> backup root: $bkproot"
echo "--> storage source: $storagesrc"
echo "--> storage dest: $storagedest"

mkdir $bkproot
mkdir -p $storagedest

time sudo rsync \
	-a \
	-v \
	--exclude **/.venv*/ \
	--exclude **/.postgres_local*/ \
	--exclude .Trash-1000/ \
	--exclude "cv - examles"/ \
	--exclude "dev"/ \
	--exclude "Dropbox/.dropbox.cache"/ \
	--exclude "Dropbox/.dropbox" \
	--exclude "foundation-trilogy_bbc-radio_1973_complete"/ \
	--exclude "Job Hunt - 2020"/ \
	--exclude "Job Hunt - 2021"/ \
	--exclude "Lenovo"/ \
	--exclude "Music/______mp3_copies"/ \
	--exclude "Records for Youtube"/ \
	--exclude "Router"/ \
	--exclude "sleep videos"/ \
	--exclude "tutorial - youtube"/ \
	--exclude "VBoxMachines"/ \
	--exclude "Youtube-DL"/ \
	$storagesrc $storagedest | tee $bkproot/RSYNC.log

echo "--> diff:"

time diff -r -q \
	-x .venv \
	-x .Trash-1000 \
	-x .postgres_local \
	$storagesrc $storagedest \
	| tee $bkproot/DIFF.log

# echo "--> checksums:"
#
# time find $storagedest -type f -exec sha512sum {} \; | tee $bkproot/CHECKSUMS.txt

echo "--> storage size:"
du -c -h -s $storagedest
echo "====================================================="
