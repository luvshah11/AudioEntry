// SDL_Test.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <stdio.h>
#include "SDL.h"
#undef main

int main()
{
	if (SDL_Init(SDL_INIT_EVERYTHING) < 0)
	{
		printf("Coudl not inititialize: %s\n", SDL_GetError());
	}
	else
	{
		printf("successfully executed");
	}
    return 0;
}

