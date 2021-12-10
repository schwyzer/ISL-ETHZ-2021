#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define MAXL 15
/*

void format(char* guess, char * user_guess, int length){
	int dollars = MAXL - length;
	int i = 0;
	for(i = 0; i < dollars; i++){
		guess[i] = '$';
	} 
	int j = 0;
	//printf("%s\n", user_guess);
	//printf("%s\n", guess);
	for(j =0; j < MAXL - length; j++){
		guess[i] = user_guess[j];
		i++;
	}
	//printf("%s\n", user_guess);
}

*/
int check_password(char* p, int p_size,  char* i, int i_size) {

	int max_length = 0; //MIN(p_size, i_size); //only check till the end of the smallest string
	int pos = 0;
	char d;
	char r;
	int out = 1; // cl ddc4  -0x0c                  rbp -> ddd0
	// i_size ddb0  -0x20
	// p_size ddb4  -0x1c
	
	//printf("%s\n", p);
	//printf("%s\n", i);
	//printf("%s\n", p);
	//printf("%s\n", i);
	asm(
		"mov -0x20(%rbp), %al \n\t \
		 mov -0x1c(%rbp), %bl \n\t \
		 mov -0x1c(%rbp), %cl \n\t \
		 cmp %al, %bl \n\t \
		 cmovl %ax, %cx \n\t \
		 mov %cl, -0x08(%rbp) \n\t \
		 xor %ax, %ax \n\t \
		 xor %bx, %bx \n\t \
		 xor %cx, %cx \n\t"
	);
	
	
	//printf("%s\n", p);
	//printf("%s\n", i);
	//printf("%d\n", max_length);
	for (pos = 0; pos < MAXL; pos++)	{
		d = p[pos]; // al ddc3  -0x0d
		r = i[pos]; // bl ddc2  -0x0e
		
		asm(
			"mov -0x0d(%rbp), %al \n\t \
			 mov -0x0e(%rbp), %bl \n\t \
			 mov -0x0c(%rbp), %cl \n\t \
			 mov $0, %dl \n\t \
			 cmp %al, %bl \n\t \
			 cmovne %dx, %cx \n\t \
			 mov %cl,-0x0c(%rbp) \n\t \
		 	 xor %al, %al \n\t \
		 	 xor %bl, %bl \n\t \
		 	 xor %cl, %cl \n\t \
		 	 xor %dl, %dl \n\t"
		);
		
	}
	/*
	asm(
		"mov -0x20(%rbp), %al \n\t \
		 mov -0x1c(%rbp), %bl \n\t \
		 mov -0x0c(%rbp), %cl \n\t \
		 mov $0, %dl \n\t \
		 cmp %al, %bl \n\t \
		 cmovne %dx, %cx \n\t \
		 mov %cl, -0x0c(%rbp) \n\t \
		 xor %ax, %ax \n\t \
		 xor %bx, %bx \n\t \
		 xor %cx, %cx \n\t \
		 xor %dx, %dx \n\t"
	);
	*/
	//printf("%x\n", out);
	return out;

}

//assumptions: password only has small characters [a, z], maximum length is 15 characters
int main (int argc, char* argv[])	{

	if (argc != 3) {
		fprintf(stderr, "Usage: %s <password guess> <output_file>\n", argv[0]);
		exit(EXIT_FAILURE);
	}


	FILE* password_file;
	char password [16] = "\0";
	char guess [16] = "\0";
	
	size_t len = 0;
	char* line;
	password_file = fopen ("/home/sgx/isl/t3_3/password.txt", "r");

	if (password_file == NULL) {
		perror("cannot open password file\n");
		exit(EXIT_FAILURE);
	}

	//fscanf(password_file, "%s", password);
	fgets(password, 16, password_file);
	//int is_match = 0; 
	printf("%s\n", password);
	//format(guess, argv[1], strlen(argv[1]));
	int i = 0;
	for(i = 0; i <  MAXL - strlen(argv[1]); i++){
		guess[i] = '$';
	} 
	int j = 0;
	//printf("%s\n", user_guess);
	//printf("%s\n", guess);
	for(j =0; j < strlen(argv[1]); j++){
		guess[i] = argv[1][j];
		i++;
	}
	//printf("%s\n", guess);
	//printf("%s\n", password);
	//is_match = check_password(password, strlen(password), guess, strlen(guess));
	
	FILE* output_file;
	output_file = fopen (argv[2], "wb");
	fputc(check_password(password, strlen(password), guess, strlen(guess)), output_file);
	fclose(output_file);

	fclose(password_file);
	return 0;
}



