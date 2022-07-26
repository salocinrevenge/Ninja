package engine;

public class GameManager implements AbstractGame
{

	public GameManager()
	{
		/* 
		 * Esse m�todo deve conter tudo que deve ser criado 
		 * ao se inicializar o jogo pela primeira vez.
		 * aqui est� contido o m�todo Menu
		 * 
		 */
		
	}
	

	public void update()
	{
		/*
		 * Esse m�todo de atualiza��o ser� chamado a cada
		 * ciclo do jogo simbolizando a passagem do tempo
		 * 
		 */
		
	}

	public void renderer(Renderer r)
	{
		/*
		 * Esse � o m�todo mostrador. Ele chama todos os outros 
		 * mostradores para serem mostrados na sa�da
		 * 
		 */

		
	}

	public static void main(String[] args)
	{
		/*
		 * Esse m�todo principal � invocado ao iniciar o jogo
		 * 
		 */
		
		GameContainer gc = new GameContainer(new GameManager());
		gc.start();
		
	}
}
