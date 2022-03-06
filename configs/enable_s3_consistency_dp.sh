

In order to enable consistent view or add any other sort of configuration, there is an option in EMR resource in data 
pipeline to add configuration where you can add EMRFS consistent property so that it would be enabled on EMR. 

To add configurations to the EMR Cluster: 

    1. Click the drop down menu next to "Add an optional field" and then select "Configuration" from the list. (Screen-shots attached)
    
    2. Then select "Create new: EmrConfiguration".
    
    3. Click "EmrConfiguration DefaultEmrConfiguration 1 "in the flowchart, specify the classification as "emrfs-site" and then select "Property" under "Add an Optional Field" drop down.   
    
    4. Under property select "Create new: Property" from drop down. 
    
    5. Now select "Property DefaultProperty1" from flow chat and then give property values as show. 
    
    Key:  fs.s3.consistent 
    Value:  true
