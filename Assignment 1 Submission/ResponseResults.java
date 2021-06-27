import java.io.*;
import java.net.*;
import java.util.Random;
import java.nio.ByteBuffer;


public class ResponseResults {
        byte[] dataRecieved;
        int[] rID = new int[2];
		int QR;
		int AA;
		int TC;
		int RD;
		int RA; 
		int RCODE;
		int QDCOUNT;
		int ANCOUNT;
		int NSCOUNT;
		int ARCOUNT;
		
		ResponseResults(DatagramPacket incomingPacket){
		this.dataRecieved = incomingPacket.getData();
		this.rID = new int[2];
		this.rID[0] = dataRecieved[0] & 0xff; //response id first half
		this.rID[1] = dataRecieved[1] & 0xff; //response id second half
		this.QR =((dataRecieved[2]>>7)&1)&0xff; //QR bit found
		this.AA =((dataRecieved[2]>>2)&1)&0xff; //AA bit found
		this.TC=((dataRecieved[2]>>1)&1)&0xff;//TC bit found
		this.RD=((dataRecieved[2]>>0)&1)&0xff;//RD bit found
		this.RA =((dataRecieved[3]>>7)&1)&0xff;//RA bit found
		this.RCODE = dataRecieved[3] & 0x0f; //RCODE byte found
		this.QDCOUNT=(short) ((dataRecieved[4] << 8) | (dataRecieved[5] & 0xFF)); // 2 bytes that make up QDCOUNT found
		this.ANCOUNT=(short) ((dataRecieved[6] << 8) | (dataRecieved[7] & 0xFF)); // 2 bytes that make up ANCOUNT found
		this.NSCOUNT=(short) ((dataRecieved[8] << 8) | (dataRecieved[9] & 0xFF)); // 2 bytes that make up ANCOUNT found
		this.ARCOUNT=(short) ((dataRecieved[10] << 8) | (dataRecieved[11] & 0xFF)); // 2 bytes that make
}


}

