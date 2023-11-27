import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)

/**
 * Write a description of class Auto here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class Auto extends Actor
{
    /**
     * Act - do whatever the Auto wants to do. This method is called whenever
     * the 'Act' or 'Run' button gets pressed in the environment.
     */
    public void turnLeft(int angulo){
        int i = getRotation();
        while(i/angulo!=1){
            Greenfoot.delay(150);
            setRotation(getRotation()+1);
            i++;
            if(getRotation()%2==0){
                move(1);   
            }
        }
    }
    
    public void turnRight(int angulo){
        int i = getRotation();
        while(i/angulo!=1){
            Greenfoot.delay(150);
            setRotation(getRotation()+1);
            i++;
            if(getRotation()%2==0){
                move(1);   
            }
        }
    }
    
}
