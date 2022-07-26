package engine;

import java.awt.image.DataBufferInt;

public class Renderer
{
	/*
	 * O desenhador cuida de desenahr os objetos na saída
	 * 
	 */
	
	private int pW; //largura do vetor de pixels
	private int pH; //altura do vetor de pixels
	private int[] p; //vetor de pixels

	
	public Renderer(GameContainer gc)
	{
        this.pW = gc.getWidth();	//largura definida no gc
        this.pH = gc.getHeight();	//altura definida no gc
        //receber o vetor de pixels da tela pricipal
        this.p = ((DataBufferInt) gc.getWindow().getImage().getRaster().getDataBuffer()).getData();
        

	}
	
	public void setPixel(int x, int y, int value)
	{
		//se fora dos limites, ou possuir a cor rosa a se retirar, não pintar o pixel
        if( (x < 0 || x >= pW || y < 0 || y >= pH) || value == 0xffff00ff) return;
        
        //pintar o pixel
        p[x + y*pW] = value;
	}

	public void clear()
	{
		//seta a tela como preta
        for(int i = 0; i < p.length; i++){
              p[i] = 0xff000000;
        }
	}
	
}
