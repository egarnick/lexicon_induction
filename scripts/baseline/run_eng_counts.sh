#!/bin/sh

chmod 744 /home2/egarnick/courses/LOR/eng_counts.sh

condor_submit eng_counts1.cmd
condor_submit eng_counts2.cmd
condor_submit eng_counts3.cmd
condor_submit eng_counts4.cmd
condor_submit eng_counts5.cmd
condor_submit eng_counts6.cmd
condor_submit eng_counts7.cmd
condor_submit eng_counts8.cmd
condor_submit eng_counts9.cmd
condor_submit eng_counts10.cmd
