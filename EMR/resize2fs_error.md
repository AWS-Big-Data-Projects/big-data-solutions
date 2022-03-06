resize2fs at time throws an error while extending the file system on AWS EMR when the EBS volumne storgae is extended( Increase capacity ) 

esize2fs 1.42.9 (28-Dec-2013) 
      resize2fs: Bad magic number in super-block while trying to open /dev/nvme0n1p1 
      Couldn't find valid filesystem superblock.
      
 Couple of commands to extend the partition:
 
 Extending a partition
      # sudo growpart /dev/xvda 1

      Extending the file system
      # sudo resize2fs /dev/xvda1

      To confirm 
      # lsblk

xfs_growfs /dev/nvme0n1p1 

check the file system type for the EBS root volume using "blkid" command

 The reason for the above error is resize2fs command works on ext4 volumes where as the filesysem XFS requires xfs_growfs. 
