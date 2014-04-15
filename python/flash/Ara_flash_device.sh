#!/bin/bash -e

# Keep code as one-liners and avoid conditions/multi-lines altogether in this file,
# so these instructions can be processes one by one by external tools.

TOP_DIR=`pwd`
OUT_DIR=`pwd`

if [[ -e default_variant.txt ]]; then
    default_variant=`cat default_variant.txt`
else
    if [[ -e $ANDROID_BUILD_TOP/device/nokia/$TARGET_PRODUCT/${TARGET_PRODUCT}.mk ]]; then
        default_variant=`perl -e '($default = \`cat $ENV{ANDROID_BUILD_TOP}/device/nokia/$ENV{TARGET_PRODUCT}/$ENV{TARGET_PRODUCT}.mk\`) =~ s/^.*?PRODUCT_DEFAULT_MULTIVARIANT.*_(\w+)\.json.*?$/$1/s; print "$default";'`
    else
        default_variant="not_found"
    fi
fi

echo "Default $default_variant"

echo "Checking flash files from current dir..."
if [ ! -e *NON-HLOS.bin ]; then
    echo "Not found!"
    echo "Checking flash files from build dir..."
    if [ -z $ANDROID_BUILD_TOP ] || [ -z $ANDROID_PRODUCT_OUT ]; then
        echo "No ANDROID_BUILD_TOP or ANDROID_PRODUCT_OUT found!"
	exit 1
    fi
    TOP_DIR=$ANDROID_BUILD_TOP/PreBuiltImages/ara
    OUT_DIR=$ANDROID_PRODUCT_OUT
fi

echo "Found!"
echo

# User is able to select proper custom image
if ls $OUT_DIR/*custom.img > /dev/null 2>&1; then
    cd $OUT_DIR; custom_list=`ls *custom.img`
fi

echo "Select custom image [Enter selects default: $default_variant]:"
n=0
for word in $custom_list
do
    n=`expr $n + 1`
    eval image$n="$word"
    if [[ $word == *$default_variant*custom.img ]]; then
	echo "  $n. $word [default]"
	default=$n
    else
	echo "  $n. $word"
    fi
done

if [[ $n > 1 ]]; then
    while [ "$custom" = "" ]
    do
        printf "Selection: "
        read count
        if [[ -z $count ]]; then
            count=$default
        fi
        eval custom=\$image$count
    done
else
    eval custom=\$image$n
fi

echo Selected image: $custom
echo

fastboot devices

fastboot    flash    modem      $TOP_DIR/*NON-HLOS.bin
fastboot    flash    sbl1       $TOP_DIR/*sbl1.mbn
fastboot    flash    sbl1bak    $TOP_DIR/*sbl1.mbn
fastboot    flash    rpm        $TOP_DIR/*rpm.mbn
fastboot    flash    rpmbak     $TOP_DIR/*rpm.mbn
fastboot    flash    tz         $TOP_DIR/*tz.mbn
fastboot    flash    tzbak      $TOP_DIR/*tz.mbn
emmc=`ls --ignore=*unsigned* $OUT_DIR | grep emmc_appsboot.mbn`
fastboot    flash    aboot      $OUT_DIR/$emmc
fastboot    flash    abootbak      $OUT_DIR/$emmc
boot=`ls --ignore=*nonsecure* $OUT_DIR | grep boot.img`
fastboot    flash    boot       $OUT_DIR/$boot
fastboot -S 200M  flash    system     $OUT_DIR/*system.img
fastboot    flash    cache      $OUT_DIR/*cache.img
fastboot    flash    userdata   $OUT_DIR/*userdata.img
recovery=`ls --ignore=*ramdisk* --ignore=*nonsecure* $OUT_DIR | grep recovery.img`
fastboot    flash    recovery   $OUT_DIR/$recovery
echo Custom image to be flashed: $custom
fastboot    flash    custom     $OUT_DIR/$custom
fastboot    flash    sdi        $TOP_DIR/*sdi.mbn


echo
echo

echo  fastboot    reboot
fastboot    reboot
