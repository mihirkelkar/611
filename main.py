#!/usr/bin/python
import sys
import mips_parser
import destination_op_finder
import raw_finder
import waw_finder
def main():
	#Read the instruction file
	code = (open(sys.argv[1], r"U")).readlines()
	parsed_code, labels  = mips_parser.mips_parse(code)
	#<-------TESTING MODULE---------------->
	#for line in parsed_code:
	#	print line
	#print labels
	#<------------------------------------->
	print "<------------------------------------------------------->"
	#Reading the data file and storing it in a list
	memory_data = [x.strip() for x in (open(sys.argv[2], r"U")).readlines()]
	#<------TESTING MODULE----------------->
	#for i in memory_data:
	#	print i
	#<------------------------------------->
	register_data = [x.strip() for x in (open(sys.argv[3])).readlines()]
	#<------TESTING MODULE----------------->
	#for i in register_data:
	#	print i

	#Find RAW Dependenies in the passed code.
	#The first thing that we need to do is to get a list of destination operands before th einstruction we are looking at. 
	#I write a function which can go thorugh the entire code in a pass and create a dictionary identifying destination operands before your level. 
	destdict =  destination_op_finder.dest_op_finder(parsed_code, labels)
	#<-----------TESTING ROUTINE---------------------->
	#for i in destdict.items():
	#	print i
	#<------------------------------------------------>
	#FINDS RAW DEPENDENCIES
	raw_dict = raw_finder.raw_finder(parsed_code, destdict, labels)

	#THE RAW FINDER RETURNS NO ENTRIES CORRESPONDING TO THOSE WHICH HAVE NO DEPENDENCIES. ADDING NONE FOR SUCH CASE
	for i in range(0, len(parsed_code)):
		if i in raw_dict.keys():
			pass
		else:
			raw_dict[i] = None
	
	#<------------------TESTING ROUTINE----------------------->
	for i in raw_dict.items():
		print i
	#<-----------------TESTING ROUTINE------------------------>
	#Find WAW HAZARDS and deal with them
	waw_dict = waw_finder.waw_finder(parsed_code, destdict, labels)
	

	#FIND WAR HAZARDS BY USING PERIPHERAL INFORMATION.
	war_dict  = war_finder.war_finder(parsed_code, destdict, labels)
if __name__ == "__main__":
	main()

