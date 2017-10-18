from collections import OrderedDict

file_name = "data/9606.protein.links.v10.5.txt"

output_file = "data/9606.protein.links.v10.5.paj"

dico_nodeID = OrderedDict()
node_id = 0
print("Generating Nodes list")
with open(file_name,'r') as f:
	f.readline()
	for line in f:
		start_id,end_id,_ = line.strip().split()
		if not(dico_nodeID.has_key(start_id)):
			dico_nodeID[start_id]=node_id
			node_id+=1
		if not(dico_nodeID.has_key(end_id)):
			dico_nodeID[end_id]=node_id
			node_id+=1

	f.close()

fout = open(output_file,'w')
fout.write("*Vertices {}\n".format(len(dico_nodeID)))
print("Writing nodes")
for node_name,node_id in dico_nodeID.items():
	fout.write(str(node_id)+" "+node_name+"\n")
print("Writing edges")
fout.write("*arcs\n")
with open(file_name,'r') as f:
	f.readline()
	for line in f:
		start_id,end_id,weight = line.strip().split()
		fout.write(" ".join(map(str,[dico_nodeID[start_id],dico_nodeID[end_id],weight]))+"\n")

	f.close()
fout.close()
