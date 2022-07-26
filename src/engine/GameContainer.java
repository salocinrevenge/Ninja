package engine;

public class GameContainer implements Runnable
{

	
	private AbstractGame game;
	private Window window;
	private String title = "Ninja";
	private int width = 540, height = 340;
	private double scale = 2;
	private boolean running = false;
	private final double UPDATE_CAP = 1.0/60.0;
	private Renderer renderer;
	private Thread thread;

	public GameContainer(AbstractGame game)
	{
        this.game = game;
	}
	

	public void start()
	{
		window = new Window(this);
        renderer = new Renderer(this);

        thread = new Thread(this);
        thread.run();
		
	}

	public void run(){
		
		running = true;
		boolean render = false;
		double firstTime  = 0;
		double lastTime   = System.nanoTime() / 1e9d;
		double passedTime = 0;
		double unprocessedTime = 0;
		
		double frameTime = 0;
		int frames = 0;
		int fps = 0;
		
		while(running){
			render = false;
			
			firstTime = System.nanoTime() / 1e9d;
			passedTime = firstTime - lastTime;
			lastTime = firstTime;
			
			unprocessedTime += passedTime;
			frameTime += passedTime;
			
			while(unprocessedTime >= UPDATE_CAP){
				unprocessedTime -= UPDATE_CAP;
				render = true;
				
				game.update();
				
				if(frameTime >= 1.0){
					frameTime = 0;
					fps = frames;
					frames = 0;
					//System.out.println("FPS: " + fps);
				}
			}
			
			if(render){
				renderer.clear();
				game.renderer(renderer);
				window.update();
				frames++;
			}
			else{
				try{
					Thread.sleep(1);
				}
				catch(InterruptedException e){
					e.printStackTrace();
				}
			}
		}
		
	}
	
	public Window getWindow()
	{
        return this.window;
	}
	
	public String getTitle()
	{
        return this.title;
	}

	public int getWidth()
	{
		return this.width;
	}

	public int getHeight() {
		
		return this.height;
	}

	public double getScale()
	{
		return this.scale;
	}

}
