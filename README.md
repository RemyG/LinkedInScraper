LinkedInScraper
===============

### About

This script retrieves the information from a resume on LinkedIn, and creates an XML file with these information.

The format of the output file is:
```
<?xml version="1.0" encoding="UTF-8"?>
<resume>
	<profile_url>Profile URL</profile_url>
    <name>
        <firstname>First name</firstname>
        <lastname>Last name</lastname>
    </name>
    <positions>
        <position>
            <title>Your title</title>
            <company>Your company</company>
            <location>The location of the company</location>
            <period>
                <from>From date</from>
                <to>To date (or Present)</to>
                <duration>Duration</duration>
            </period>
            <description>The job description</description>
        </position>
        <position>...</position>
        ...
    </positions>
    <languages>
        <competency>
            <language>Language name</language>
            <proficiency>Proficiency description</proficiency>
        </competency>
        <competency>...</competency>
        ...
    </languages>
    <education>
        <position>
            <summary>Summary</summary>
            <degree>Degree</degree>
            <major>Major</major>
            <period>
                <from>From date</from>
                <to>To date</to>
            </period>
            <details>Details</details>
        </position>
        <position>...</position>
        ...
    </education>
    <skills>
		<skill>Skill name</skill>
		<skill>...</skill>
		...
	</skills>
</resume>
```
The descriptions are escaped for HTML entities.

### Installation

To install this script, you'll need (of course) to have Python installed.

The modules needed to run this script are:
- cgi
- codecs
- urllib2
- requests (to install: sudo pip install requests)
- StringIO
- sys
- lxml (to install: sudo apt-get install python-lxml)

### Usage

To use this script, just run `./linkedin.py <profile_address> <output_file>`

This will scrape the information present on the LinkedIn profile at `profile_address`, and write them as XML in a new file `output_file`.

