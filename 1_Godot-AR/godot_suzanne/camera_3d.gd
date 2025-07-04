extends Camera3D

var server: UDPServer
var packet
var tx ; var ty ; var tz
var r1x ; var r1y; var r1z
var r2x ; var r2y ; var r2z
var r3x ; var r3y ; var r3z
var basis_x ; var basis_y ; var basis_z
var basis_r ; var t_vec

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	server = UDPServer.new()
	server.listen(4240)

func _data_from_packet(data:PackedByteArray) -> Dictionary:
	var json_string = data.get_string_from_utf8()
	var json = JSON.new()
	var error = json.parse(json_string)
	assert(error == OK)
	var data_received = json.data
	assert(typeof(data_received) == TYPE_DICTIONARY)
	return data_received

func server_python():
	server.poll()
	if server.is_connection_available():
		var peer: PacketPeerUDP = server.take_connection()
		var packet = peer.get_packet()
	return packet
	
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	server.poll()
	
	if server.is_connection_available():
		var peer = server.take_connection()
		var data = peer.get_packet()
		var tmat = _data_from_packet(data)
		
		tx = tmat["tx"] ; ty = tmat["ty"] ; tz = tmat["tz"]
		t_vec = Vector3(tx,ty,tz)
		
		r1x = tmat["r1x"] ; r1y = tmat["r1y"] ; r1z = tmat["r1z"]  
		r2x = tmat["r2x"] ; r2y = tmat["r2y"] ; r2z = tmat["r2z"]  
		r3x = tmat["r3x"] ; r3y = tmat["r3y"] ; r3z = tmat["r3z"]
		basis_x = Vector3(r1x,r1y,r1z)
		basis_y = Vector3(r2x,r2y,r2z)
		basis_z = Vector3(r3x,r3y,r3z)
		
		basis_r = Basis(basis_x, basis_y, basis_z)

		transform.basis = basis_r
		transform.origin = t_vec
		rotate_object_local(Vector3(1, 0, 0), PI)
		
