"""
gff_to_gtf - Python library for converation of annotation files from gff format to gtf
"""

__version__ = "0.1.0"

import argparse

def generate_dictionary_of_ids(annotation_file, annotation_format):
	"""
	Return a dictionary of gene_id/Parent : transcript_id/ID.
	
	:annotation_file: file with information about gene_id/Parent : transcript_id/ID.
	:annotation_format: gtf or gff
	"""
	gene_transcript_dic = {}
	for line in open(annotation_file):
		if annotation_format == "gtf":
			nine_col = line.split()[8]
			transcript = nine_col.split(";")[0].strip("transcript_id ")
			gene = nine_col.split(";")[1].strip("\n").strip("gene_id ")
			gene_transcript_dic[transcript] = gene
		elif annotation_format == "gff":
			nine_col = line.split()[8]
			transcript = nine_col.split(";")[0].strip("ID=")
			gene = nine_col.split(";")[1].strip("\n").strip("Parent=")
			gene_transcript_dic[transcript] = gene
		else:
			print("invalid annotation format")
	return gene_transcript_dic
			

def gff_to_gtf_convertation(input_gff, output_gff_name, gene_transcript_dic):
	"""
	Return a gtf file
	
	:input_gff: gff file
	:output_gff_name: name of output file
	"""
	with open(output_gff_name, "w") as record_file:
		for line in open(input_gff, "r"):
			
			third_col = line.split()[2]
			
			if third_col == "five_prime_UTR":
				third_col = "5UTR"
			elif third_col == "three_prime_UTR":
				third_col = "3UTR"
			one_two = line.split()[0:2]
			four_eight = line.split()[3:8]
			nine_col = line.split()[8]
			transcript = nine_col.split(";")[0].strip("ID=").strip("\n")
			print(transcript)
			gene = gene_transcript_dic[transcript]
			full_line = "\t".join(one_two) + "\t" + third_col + "\t" + "\t".join(four_eight) + "\t" + "gene_id " + gene + "; " +  "transcript_id " + transcript + ";"  + '\n';
			record_file.write(full_line)







def main():
	parser = argparse.ArgumentParser(description='gff_to_gtf_convertation')
	parser.add_argument('-a','--annotation_file',type=str, help='file to create mapping transcript_id/ID with gene_id/Parent')
	parser.add_argument('-i','--input_file', type=str, help='input gff file with at least "ID=" in nineth column')
	parser.add_argument('-f', '--annotation_format',type=str, help='format for annotation file')
	parser.add_argument('-o', '--outfile_name',type=str,help='name of outfile')
	args = parser.parse_args()
	gene_transcript_dic = generate_dictionary_of_ids(args.annotation_file, args.annotation_format)
	print(gene_transcript_dic)
	gff_to_gtf_convertation(args.input_file, args.outfile_name, gene_transcript_dic)
   

if __name__ == "__main__":
   main()
