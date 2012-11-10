/*** Definition section ***/

%{
/* C code to be copied verbatim */
#include <stdio.h>
%}

/* This tells flex to read only one input file */
%option noyywrap

%%
    /*** Rules section ***/

    /* [0-9]+ matches a string of one or more digits */
[0-9]+  {
            /* yytext is a string containing the matched text. */
            printf("Saw an integer: %s\n", yytext);
        }

.|\n    {   /* Ignore all other characters. */   }

%%
/*** C Code section ***/

int main(void)
{
    /* Call the lexer, then quit. */
    yylex();
    return 0;
}

/***
	If this input is given to flex, it will be converted into a C file, lex.yy.c. 
	This can be compiled into an executable which matches and outputs strings of integers. 
	For example, given the input:
	abc123z.!&*2gj6
	the program will print:
	Saw an integer: 123
	Saw an integer: 2
	Saw an integer: 6
***/