package probMissionariosCanibais;

import java.util.ArrayList;
import java.util.List;

public class Estado {

    int missionariosEsq;
    int canibaisEsq;
    int missionariosDir;
    int canibaisDir;
    boolean barcoEsq;

    Estado pai; //  aqui é pra guardar o caminho, adicionei essa parte depois, quando vi que eu nçao estava mostrando os caminhos

    // construtor
    public Estado(int missionariosEsq, int canibaisEsq,
                  int missionariosDir, int canibaisDir,
                  boolean barcoEsq) {

        this.missionariosEsq = missionariosEsq;
        this.canibaisEsq = canibaisEsq;
        this.missionariosDir = missionariosDir;
        this.canibaisDir = canibaisDir;
        this.barcoEsq = barcoEsq;
        this.pai = null; // começa sem pai
    }

    // aqui to verificando se chegou no Obj.
    public boolean isObjetivo() {
        return missionariosEsq == 0 && canibaisEsq == 0;
    }

    // verifica se o estado é válido
    public boolean isValido() {

        if (missionariosEsq < 0 || canibaisEsq < 0 ||
                missionariosDir < 0 || canibaisDir < 0) {
            return false;
        }

        if (missionariosEsq > 0 && canibaisEsq > missionariosEsq) {
            return false;
        }

        if (missionariosDir > 0 && canibaisDir > missionariosDir) {
            return false;
        }

        return true;
    }

    // gera próximos estados
    public List<Estado> gerarProximos() {

        List<Estado> lista = new ArrayList<>();

        int[][] movimentos = {
                {1, 0},
                {2, 0},
                {0, 1},
                {0, 2},
                {1, 1}
        };

        for (int i = 0; i < movimentos.length; i++) {

            int m = movimentos[i][0];
            int c = movimentos[i][1];

            Estado novo;

            if (barcoEsq) {
                novo = new Estado(
                        missionariosEsq - m,
                        canibaisEsq - c,
                        missionariosDir + m,
                        canibaisDir + c,
                        false
                );
            } else {
                novo = new Estado(
                        missionariosEsq + m,
                        canibaisEsq + c,
                        missionariosDir - m,
                        canibaisDir - c,
                        true
                );
            }

            if (novo.isValido()) {
                novo.pai = this; // 👈 AQUI LIGA OS ESTADOS
                lista.add(novo);
            }
        }

        return lista;
    }

    public String toString() {
        return "(" + missionariosEsq + "," + canibaisEsq + " | "
                + missionariosDir + "," + canibaisDir + " | "
                + (barcoEsq ? "E" : "D") + ")";
    }
}