%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define YYDEBUG 1

int production_string[300];
int production_string_length = 0;

void addToProductionString(int production_number) {
        production_string[production_string_length++] = production_number;
}

void printProductionString() {
        int index;
        for(index = 0; index < production_string_length - 1; index++){
                printf("P%d -> ", production_string[index]);
        }
        printf("P%d ", production_string[index]);
        printf("\n");
}
%}

%token NOT
%token AND
%token OR
%token XOR
%token LET
%token CHECK
%token ELSECHECK
%token ELSE
%token FOR
%token WHILE
%token INTEGER
%token STRING
%token BOOL
%token CHAR
%token WRITE
%token READ
%token ID
%token CONST
%token HASH
%token QUESTIONMARK
%token OPENPARA
%token CLOSEDPARA
%token OPENSQUAREPARA
%token CLOSEDSQUAREPARA
%token OPENCURLYPARA
%token CLOSEDCURLYPARA
%token SEMICOLON
%token COLON
%token POINT
%token COMMA
%token PLUS
%token MINUS
%token MUL
%token DIV
%token MOD
%token POW
%token EQUAL
%token EQUALEQUAL
%token LESS
%token LESSEQUAL
%token GREATER
%token GREATEREQUAL
%token NOTEQUAL
%left '+' '-' '*' '/' '^'

%start program

%%
program : HASH cmpdstmt QUESTIONMARK {addToProductionString(1);}
	;
declaration :  LET ID COLON type {addToProductionString(2);}
	    ;
type :  INTEGER {addToProductionString(3);} | STRING {addToProductionString(4);} | CHAR {addToProductionString(5);} | BOOL {addToProductionString(6);}
	   ;
cmpdstmt : OPENCURLYPARA stmts CLOSEDCURLYPARA {addToProductionString(7);}
	 ;
stmts : stmt {addToProductionString(8);} | stmt stmts {addToProductionString(9);}
    ;
stmt :  assignment SEMICOLON {addToProductionString(10);} | declaration SEMICOLON {addToProductionString(11);} | forstmt SEMICOLON {addToProductionString(12);} | checkstmt SEMICOLON {addToProductionString(13);} | whilestmt SEMICOLON {addToProductionString(14);} | readstmt SEMICOLON {addToProductionString(15);} | writestmt SEMICOLON {addToProductionString(16);}
	 ;
assignment : ID EQUAL expr {addToProductionString(17);}
    ;
expr : expr PLUS term {addToProductionString(18);} | expr MINUS term {addToProductionString(19);} | term {addToProductionString(20);}
    ;
term : term MUL factor {addToProductionString(21);} | term DIV factor {addToProductionString(22);} | term MOD factor {addToProductionString(23);} | factor {addToProductionString(24);}
    ;
factor : OPENPARA expr CLOSEDPARA {addToProductionString(25);} | ID {addToProductionString(26);} | INTEGER {addToProductionString(27);} | CONST {addToProductionString(28);}
    ;
cond : expr relation expr {addToProductionString(29);}
    ;
condstmt : cond {addToProductionString(30);} | cond logical cond {addToProductionString(31);} | NOT cond {addToProductionString(32);}
    ;
relation : LESS {addToProductionString(33);} | LESSEQUAL {addToProductionString(34);} | GREATER {addToProductionString(35);} | GREATEREQUAL {addToProductionString(36);} | NOTEQUAL {addToProductionString(37);} | EQUALEQUAL {addToProductionString(38);}
    ;
forstmt : FOR OPENPARA assignment SEMICOLON condstmt SEMICOLON assignment CLOSEDPARA cmpdstmt {addToProductionString(39);}
checkstmt : CHECK OPENPARA condstmt CLOSEDPARA cmpdstmt {addToProductionString(40);} | CHECK OPENPARA condstmt CLOSEDPARA cmpdstmt OPENCURLYPARA ELSECHECK OPENPARA condstmt cmpdstmt CLOSEDCURLYPARA {addToProductionString(41);} | CHECK OPENPARA condstmt CLOSEDPARA cmpdstmt OPENCURLYPARA ELSECHECK OPENPARA condstmt CLOSEDPARA cmpdstmt CLOSEDCURLYPARA ELSE cmpdstmt {addToProductionString(42);} | CHECK OPENPARA condstmt CLOSEDPARA cmpdstmt ELSE cmpdstmt {addToProductionString(43);}
    ;
whilestmt : WHILE OPENPARA condstmt CLOSEDPARA cmpdstmt {addToProductionString(44);}
    ;
readstmt : READ OPENPARA ID CLOSEDPARA {addToProductionString(45);}
    ;
writestmt : WRITE OPENPARA expr CLOSEDPARA {addToProductionString(46);}
    ;
logical : AND | OR | XOR {addToProductionString(47);}
    ;

%%
yyerror(char *s)
{
	printf("%s\n",s);
}

extern FILE *yyin;

main(int argc, char **argv)
{
	if(argc>1) yyin :  fopen(argv[1],"r");
	if(argc>2 && !strcmp(argv[2],"-d")) yydebug: 1;
	if(!yyparse()) printProductionString();
}
