#include <iostream>		//cout
#include <stdlib.h> 	//system
#include <unistd.h>		//sleep
#include <fstream>      //ifstream
#include <string.h>		//memcpy

using namespace std;

int main(){	

	while(true){

		system("cat /etc/passwd | cut -d: -f1 > usuario.txt");
		ifstream is("usuario.txt");   // open file
		
		string user, userTmp;

		while(!is.eof()){
			userTmp = user; //string usada para não haver repetição do total de processos do último usuário

			is >> user;
			
			if(user != userTmp){
				string comando =  "ps -f -u " + user + " | wc -l";

				//converter string para char*
				char *comandoFinal = new char[comando.length()+1];
				memcpy(comandoFinal, comando.c_str(), comando.length() + 1);

				cout << "Total de processos do usuário " << user << endl;
				system(comandoFinal);
			}
		}
		cout << "Total de Processos: " << endl; 
		system("ps aux | wc -l");	

		cout << endl << "Recarregando...." << endl;
		sleep(5);//dormir por 5 segundos
	}	

	return 0;
}
