package game;

import engine.Renderer;

public class Menu {

	private MenuStates state;
	
	public Menu()
	{
		this.state = MenuStates.MAIN;
	}
	
	public void render(Renderer r)
	{
		switch(this.state)
		{
		case MAIN:
			{
				
			}
			break;
		case GAME:
			{
				
			}
			break;
		
		default:
			//TODO: excessão aqui
			break;
		
		}
		
	}
	
	public void tick()
	{
		switch(this.state)
		{
		case MAIN:
			{
				
			}
			break;
		case GAME:
			{
				
			}
			break;
		
		default:
			//TODO: excessão aqui
			break;
		
		}
	}
	
	
}
