import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)

/**
 * Write a description of class MyWorld here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class MyWorld extends World
{
    int ejecucion=0;
    Auto autito = new Auto();
    public MyWorld()
    {    
        super(600, 400, 1); 
        addObject(autito, 300,200);
        
    }
    public void act(){
        if (ejecucion==0){
            movimiento();
        }
    }
    public void movimiento(){
        //instrucciones
        ejecucion++;
    }
}
