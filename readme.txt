Add lightroom XMP scripting: 3 parts are all completed by user in a single frame
1. read the XMPs to a spreadsheet / dataframe
2. modify the dataframe
    - sort dataframe by capture moment
    - add and delete tags, use tags for everything from keyframes to day/night to every fourth/tenth/20th photo feature
3. write the changes (changes only?) to the XMPs
 
Lightroom time lapse functions:
1.
- Read the XMPs, all of the fields of specific headings, like the heading "CRS" for example.
- Save a snapshot dataframe as CSV.
- Format the data in the dataframe to usable format, like float instead of text.
 
2.
- interpolate between keyframes
- write keywords kfstart, kfmid, kfend, flagged, night, day, civiltwilight, nauticaltwilight, astronomicaltwilight, sunset, sunrise, moonset, moonrise
- 
 
3.
- Compare changed dataframe to the snapshot and identify the differences.
- Format data as text that matches the exact format Lightroom uses.
- Write the changes.
 
Other functions:
- Modify filenames of folders full of image files.
 
README:
- Interfaces only with text within the XMP files
- User needs to use only the read from metadata and write to metadata features in Lightroom
- Screenshots from Lightroom, to include setting to save XMP files by default.
 
AWIM:
- eliminate saving metadata to RAW file requirement because it doesn't make sense.
- Camera AWIM tag should be JSON of dictionary. No pickle at all.
- generate_camera_AWIM_from_calibration should generate a JSON text file, not an image. The JSON tag should be the same for the calibration image as it is for any AWIM tagged image.
- All interface with Astropy should be with dataframes of requests, not individual requests - I think.
- Convert entirely to pyexiv2 - I think - to preserve resolution of imgages.