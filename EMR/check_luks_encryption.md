When you use LUKS encryption, though your EBS volumes are encrypted along with any instance store volumes, you still see EBS with Not Encrypted status when you use an Amazon EC2 API or the EC2 console to check on the encryption status. This is because the API doesn’t look into the EMR cluster to check the disk status; your auditors would need to SSH into the cluster to check for disk encrypted compliance. However, with EBS encryption, you can check the encryptions status from the EC2 console or through an EC2 API call.


Commands to check once you perform ssh on the master/core/task node of an AWS EMR cluster : 

1. Perform sudo su 
2. Execute the command - lsblk - Running lsblk on the cluster will only check the status of LUKS encryption.
3. Running lsblk will output the below as an example : 

          NAME          MAJ:MIN RM SIZE RO TYPE  MOUNTPOINT
          nvme1n1       259:0    0  32G  0 disk  
          ├─nvme1n1p1   259:5    0   5G  0 part  
          │ └─nvme1n1p1 253:0    0   5G  0 crypt /emr
          └─nvme1n1p2   259:6    0  27G  0 part  
            └─nvme1n1p2 253:1    0  27G  0 crypt /mnt
          nvme2n1       259:1    0  32G  0 disk  
          └─nvme2n1     253:2    0  32G  0 crypt /mnt1
          nvme0n1       259:2    0  17G  0 disk  
          ├─nvme0n1p1   259:3    0  17G  0 part  /
          └─nvme0n1p128 259:4    0   1M  0 part 

4. In the above , it shows the following are LUKS encrypted : /dev/nvme1n1p1 , /dev/nvme1n1p2 and /dev/nvme2n1 . Like I mentioned and also pointed out by the previous engineer when using LUKS encryption additional steps provided must be taken to encrypt root volume as we can see above root volume "nvme0n1p1" is not encrypted.

5. Additionally you can run these following commands as well to verify LUKS encryption on these volumes. As an example , below are the steps I took to verify on my AWS cluster I tested out: 

    [root@ip-xxx-xx-xx-xxx hadoop]# cryptsetup isLuks /dev/nvme1n1p1 && echo "$DEV_LUKS is a LUKS Device" || echo "$DEV_LUKS is not a LUKS Device"
    /dev/xvda is a LUKS Device
    [root@ip-xxx-xx-xx-xxx hadoop]# 
    [root@ip-xxx-xx-xx-xxx hadoop]# 
    [root@ip-xxx-xx-xx-xxx hadoop]# cryptsetup isLuks /dev/nvme1n1p2 && echo "$DEV_LUKS is a LUKS Device" || echo "$DEV_LUKS is not a LUKS Device"
    /dev/xvda is a LUKS Device
    [root@ip-xxx-xx-xx-xxx hadoop]# 
    [root@ip-xxx-xx-xx-xxx hadoop]# 
    [root@ip-xxx-xx-xx-xxx hadoop]# cryptsetup isLuks /dev/nvme2n1 && echo "$DEV_LUKS is a LUKS Device" || echo "$DEV_LUKS is not a LUKS Device"
    /dev/xvda is a LUKS Device
    
    https://aws.amazon.com/blogs/big-data/best-practices-for-securing-amazon-emr/
    
    
    https://aws.amazon.com/blogs/big-data/secure-your-data-on-amazon-emr-using-native-ebs-and-per-bucket-s3-encryption-options/
