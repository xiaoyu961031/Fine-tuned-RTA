#!/usr/bin/env perl

use strict;
use warnings;
use Getopt::Long;
use MaterialsScript qw(:all);
use IO::Handle;

###ACTION### User Input Section ##############################

#Specify where the target molecules are
my $RootDir = "/hpctmp/xiaoyu96/";

my $TargetDir = "work_job_split_171269/";

# This is where CSP structures are; hash/comment out accordingly
my $StartStrucDir = "xsd_prased/";

# File type for molecular structures; e.g., pdb, xsd, etc.
my $FileType = "xsd";

my $forcite_quality = "Ultra-fine";
my $forcite_optimizer = "Smart";

my $forcite_forcefield = "Dreiding";
my $forcite_charge = "Use current";


my $directory = $RootDir.$TargetDir;

opendir(DIR, $directory.$StartStrucDir) or die("Could not opendir ".$directory.$StartStrucDir);
my @files = grep(/\.$FileType$/, readdir(DIR));
closedir(DIR);

foreach my $file (@files) {



	eval {
			chomp($file);
			print "Converting $file...\n";
			my $doc0 = Documents->Import($directory.$StartStrucDir.$file);
			
			$doc0->MakeP1;
			my $results = $doc0->CalculateBonds(Settings());
			my $results1 = Modules->Forcite->GeometryOptimization->Run($doc0, Settings(
				Quality => $forcite_quality, 
				CurrentForcefield => $forcite_forcefield, 
				ChargeAssignment => $forcite_charge, 
				MaxIterations => 500,
				OptimizeCell => "No",
				OptimizationAlgorithm => $forcite_optimizer,));

			$doc0->Export($directory."GeomOpted_cif/". $doc0->Name . ".cif");
			$doc0->Close;
		};
	if ($@) {
		print "Error processing $file: $@\n";
	} else {
		print "Processing of $file completed successfully\n";
	}
	# Clean up
	
}