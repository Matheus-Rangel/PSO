#include <iostream>		//cout
#include <stdlib.h>		//system
#include <string.h>		//memcpy

using namespace std;

int main(int argc, char ** argv){	


	if(argc > 1){	
		string processo  = argv[1];
		string comando = "pstree -p -s " + processo;

		if(argv[2] != NULL && argv[2][1] == 's'){
			string saida = " > saida.txt";
			comando = comando + saida;
			cout << "Arquivo saida.txt foi gerado com a saída do programa!" << endl;
		}

		//converter string para char*
		char *comandoFinal = new char[comando.length()+1];
		memcpy(comandoFinal, comando.c_str(), comando.length() + 1);

		system(comandoFinal);

	}else{
		cout << "Erro ao executar o programa!" << endl;
		cout << "Use: ./executavel numero_do_processo -s" << endl;
		cout << "-s: parâmetro opcional para gerar um arquivo com a saída do programa." << endl;
	}	
	
	return 0;
}