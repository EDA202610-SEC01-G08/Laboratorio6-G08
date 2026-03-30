"""
Script para ejecutar pruebas de rendimiento automatizadas
con diferentes factores de carga y mecanismos de colisión
"""
import sys
import time
import tracemalloc
from App import logic

def run_performance_test(map_type, load_factor, run_number):
    """
    Ejecuta una prueba de rendimiento con el tipo de mapa y factor de carga dados
    
    Args:
        map_type: 'LP' para linear probing, 'SC' para separate chaining
        load_factor: factor de carga a usar
        run_number: número de ejecución (para tracking)
    
    Returns:
        tuple: (tiempo_ms, memoria_kb, books, authors, tags, book_tags)
    """
    print(f"\n{'='*60}")
    print(f"Ejecutando: {map_type} | Factor: {load_factor} | Run: {run_number}")
    print(f"{'='*60}")
    
    # Crear catálogo con el factor de carga específico
    catalog = logic.new_logic_with_params(map_type, load_factor)
    
    # Medir carga de datos
    books, authors, tags, book_tags, tiempo, memoria = logic.load_data(catalog)
    
    print(f"Libros: {books}, Autores: {authors}, Tags: {tags}, BookTags: {book_tags}")
    print(f"Tiempo: {tiempo:.2f} ms | Memoria: {memoria:.2f} kB")
    
    return tiempo, memoria, books, authors, tags, book_tags

def run_multiple_tests(map_type, load_factor, num_runs=3):
    """
    Ejecuta múltiples pruebas y retorna el promedio
    """
    tiempos = []
    memorias = []
    
    for i in range(1, num_runs + 1):
        tiempo, memoria, books, authors, tags, book_tags = run_performance_test(map_type, load_factor, i)
        tiempos.append(tiempo)
        memorias.append(memoria)
        
        # Esperar un poco entre ejecuciones
        time.sleep(2)
    
    tiempo_promedio = sum(tiempos) / len(tiempos)
    memoria_promedio = sum(memorias) / len(memorias)
    
    print(f"\n{'='*60}")
    print(f"PROMEDIO - {map_type} | Factor: {load_factor}")
    print(f"Tiempo: {tiempo_promedio:.2f} ms | Memoria: {memoria_promedio:.2f} kB")
    print(f"{'='*60}\n")
    
    return tiempo_promedio, memoria_promedio

def main():
    print("\n" + "="*60)
    print("PRUEBAS DE RENDIMIENTO - LABORATORIO 6")
    print("="*60)
    
    # Tabla 2: Linear Probing
    print("\n\n### TABLA 2: LINEAR PROBING ###\n")
    lp_factors = [0.1, 0.5, 0.7, 0.9]
    lp_results = []
    
    for factor in lp_factors:
        tiempo, memoria = run_multiple_tests('LP', factor, num_runs=3)
        lp_results.append((factor, memoria, tiempo))
    
    # Tabla 3: Separate Chaining
    print("\n\n### TABLA 3: SEPARATE CHAINING ###\n")
    sc_factors = [2.0, 4.0, 6.0, 8.0]
    sc_results = []
    
    for factor in sc_factors:
        tiempo, memoria = run_multiple_tests('SC', factor, num_runs=3)
        sc_results.append((factor, memoria, tiempo))
    
    # Imprimir resultados finales
    print("\n\n" + "="*60)
    print("RESULTADOS FINALES")
    print("="*60)
    
    print("\nTabla 2. Mediciones de tiempo y datos para diferentes factores de carga en PROBING:")
    print(f"{'Factor de Carga (LP)':<25} {'Consumo de Datos [kB]':<25} {'Tiempo [ms]':<20}")
    print("-" * 70)
    for factor, memoria, tiempo in lp_results:
        print(f"{factor:<25} {memoria:<25.2f} {tiempo:<20.2f}")
    
    print("\n\nTabla 3. Mediciones de tiempo y datos para diferentes factores de carga en CHAINING:")
    print(f"{'Factor de Carga (SC)':<25} {'Consumo de Datos [kB]':<25} {'Tiempo [ms]':<20}")
    print("-" * 70)
    for factor, memoria, tiempo in sc_results:
        print(f"{factor:<25} {memoria:<25.2f} {tiempo:<20.2f}")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
