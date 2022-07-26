package engine;

public class GameManager implements AbstractGame
{

	public GameManager()
	{
		/* 
		 * Esse método deve conter tudo que deve ser criado 
		 * ao se inicializar o jogo pela primeira vez.
		 * aqui está contido o método Menu
		 * 
		 */
		
	}
	

	public void update()
	{
		/*
		 * Esse método de atualização será chamado a cada
		 * ciclo do jogo simbolizando a passagem do tempo
		 * 
		 */
		
	}

	public void renderer(Renderer r)
	{
		/*
		 * Esse é o método mostrador. Ele chama todos os outros 
		 * mostradores para serem mostrados na saída
		 * 
		 */

		
	}

	public static void main(String[] args)
	{
		/*
		 * Esse método principal é invocado ao iniciar o jogo
		 * 
		 */
		
		GameContainer gc = new GameContainer(new GameManager());
		gc.start();
		
	}
}
