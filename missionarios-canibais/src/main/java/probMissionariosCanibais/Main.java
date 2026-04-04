package probMissionariosCanibais;

import java.util.*;

public class Main {

    public static void main(String[] args) {

        Estado inicial = new Estado(3, 3, 0, 0, true);
        // tive que aprender a usar fila, sabia só em java
        Queue<Estado> fila = new LinkedList<>();
        Set<String> visitados = new HashSet<>();

        fila.add(inicial);

        System.out.println("Iniciando busca...\n");

        while (!fila.isEmpty()) {

            Estado atual = fila.poll();

            if (visitados.contains(atual.toString())) {
                continue;
            }

            visitados.add(atual.toString());

            System.out.println("Estado atual: " + atual);

            if (atual.isObjetivo()) {

                System.out.println("\nSOLUÇÃO ENCONTRADA!\n");

                // 👇 MOSTRAR CAMINHO
                List<Estado> caminho = new ArrayList<>();

                Estado aux = atual;

                while (aux != null) {
                    caminho.add(aux);
                    aux = aux.pai;
                }

                // inverter (pra ficar do início --> fim)
                Collections.reverse(caminho);

                System.out.println("CAMINHO DA SOLUÇÃO:\n");

                for (Estado e : caminho) {
                    System.out.println(e);
                }

                break;
            }

            List<Estado> proximos = atual.gerarProximos();

            for (Estado e : proximos) {
                fila.add(e);
            }
        }
    }
}