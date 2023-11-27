#=============ACLARACION NECESARIA!!!!======================
#ESTE CODIGO TOMARA LAS INSTRUCCIONES ESCRITAS 
#EN UN ARCHIVO LLAMADO programaSinCompilar.txt y si este 
#tiene una sintaxis y semantica correctos creara un archivo 
# nuevo llamado programaCompilado.txt

import ply.lex as lex
import ply.yacc as yacc
error=False

# Lista de tokens
tokens = (
    'MOVE',
    'MOVEDIR',
    'TURN',
    'TURNDIR',
    'ARGUMENT',
    'START',
    'STOP',
    'NEWROAD',
    'REFERENCEROAD'
)

# Reglas de expresiones regulares para tokens simples
t_MOVE = r'Move'
t_MOVEDIR = r'(Forward|Backward)'
t_TURN = r'Turn'
t_TURNDIR = r'(Left|Right)'
t_ARGUMENT = r'\[\d+\];\s*\n'
t_START = r'Start;\s*\n'
t_STOP = r'Stop;\s*\n'
t_NEWROAD = r'Nroad\s[A-Z][a-zA-Z]+\:\s*\n'
t_REFERENCEROAD = r'\#[A-Z][a-zA-Z]+;\s*\n'

def t_error(t):
    print(f"Hay un caracter : '{t.value[0]}' que no conforma una instruccion valida")
    t.lexer.skip(1)
    global error
    error=True

# Error rule for syntax errors
def p_error(p):
    print("El programa ingresado no compilara")
    global error
    error=True

# Construir el lexer
lexer = lex.lex()

def p_expression(p):
    '''
    expression : NEWROAD recorrido STOP expression
               | START recorrido STOP
    '''
    if len(p)==4: 
        p[0] = [p[1], p[2]]+ [p[3]]
    elif len(p)==5: 
        p[0] = [p[1], p[2], p[3]]+ list(p[4])

def p_recorrido(p): 
    '''
    recorrido : instruccion 
              | instruccion recorrido
    '''
    if len(p)==3:
        p[0]=[p[1]]+list(p[2])
    elif len(p)==2:
        p[0]=[p[1]]


def p_instruccion(p): 
    '''
    instruccion : MOVE MOVEDIR ARGUMENT
                | TURN TURNDIR ARGUMENT 
                | REFERENCEROAD
    '''
    if len(p)==4:
        p[0]=(p[1], p[2], p[3])
    elif len(p)==2:
        p[0]=p[1]


# Construir el parser
parser = yacc.yacc()
with open('programaSinCompilar.txt','r') as a:
    s=a.read()

result = parser.parse(s)

def palabrasReservada():
    reservadas=[
        'Move',
        'Forward',
        'Backward',
        'MoveForward',
        'MoveBackward',
        'Turn',
        'Left',
        'Right',
        'TurnLeft',
        'TurnRight',
        'Start',
        'Stop',
        'Nroad'
    ]
    nombre=[]
    for i in result:
        if i[0:5]=='Nroad':
            if i[6:-1] in reservadas:
                p_error(result)
            else:
                nombre.append(i[6:-2])
    return nombre

def traerRuta(nombreDeLaRuta, ordenes, nombresExistentes):
    for i, instruccion in enumerate(result):
        if instruccion=='Nroad '+nombreDeLaRuta+':\n':
            for j in result[i + 1]:
                if j[0]=='#':
                    nombre_referencia = j[1:-2]
                    if nombre_referencia in nombresExistentes:
                        ordenes = traerRuta(nombre_referencia, ordenes, nombresExistentes)
                    else:
                        p_error(result)
                else:
                    ordenes.append(j)
            break
    return ordenes

def acomodarInstrucciones(nombresExistentes):
    ordenes = []
    for i, instruccion in enumerate(result):
        if instruccion[0:5]=='Start':
            for j in result[i + 1]:
                if j[0]=='#':
                    nombre_referencia = j[1:-2]
                    if nombre_referencia in nombresExistentes:
                        ordenes = traerRuta(nombre_referencia, ordenes, nombresExistentes)
                    else:
                        p_error(result)
                else:
                    ordenes.append(j)
    return ordenes

if not error: 
    nombresReservados = palabrasReservada()
    ordenes = acomodarInstrucciones(nombresReservados)
if not error:
    programa = open('MyWorld.java', 'w')

    programa.writelines(
        '''
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
        super(1000, 600, 1); 
        addObject(autito, 300,200);
        
    }
    public void act(){
        if (ejecucion==0){
            movimiento();
        }
    }
    public void movimiento(){
'''
    )

    for i in ordenes: 
        aux = i[0]+i[1]+i[2]
        print('The car was ' + i[0] + " " + i[1] + " " + (i[2])[1:-3] + ' meters' )
        aux=aux.replace('[','(')
        aux=aux.replace(']',')')
        aux='\t\tautito.' + aux[0].lower() + aux[1:]
        programa.writelines(aux)
    

    programa.writelines(
        '''
    ejecucion++;
    }
}
'''
    )
    programa.close()
