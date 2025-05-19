/*====Corycle====*/
#include<bits/stdc++.h>
#define ll long long
using namespace std;
const int inf = 0x3f3f3f3f;
const int N = 50;
int read() {
    int s = 0, f = 1; char c = getchar();
    while (c < '0' || c>'9') { if (c == '-')f = -1; c = getchar(); }
    while (c >= '0' && c <= '9') { s = s * 10 + c - '0'; c = getchar(); }
    return s * f;
}
int cnt[N], b[N];
int Rand() { return rand() * rand() + rand(); }
int Random(int n) { return Rand() % n + 1; }
struct Player {
    int id, up, pos;
    string name;
    Player(string Name = "default", int ID = 0, int Up = 0, int Pos = 0) :id(ID), name(Name), up(Up), pos(Pos) {}

}a[N];
void Init() {
    a[1] = Player("¿¨¿¨ÂÞ", 1, 0, 0);
    a[2] = Player("çæÀ³Ëþ", 2, 0, -1);
    a[3] = Player("³¤  Àë", 3, 2, -1);
    a[4] = Player("½ñ  Ï«", 4, 0, -2);
    a[5] = Player("  ´»  ", 5, 4, -2);
    a[6] = Player("ÊØ°¶ÈË", 6, 0, -3);
    for (int i = 1; i <= 6; i++)b[i] = i;
}
void Move(int id, int x) {
    for (int i = 1; i <= 6; i++) {
        if (a[i].up == id)a[i].up = 0;
    }
    for (int i = 1; i <= 6; i++) {
        if (a[i].up == 0 && a[i].pos == a[id].pos + x) {
            a[i].up = id;
            break;
        }
    }
    a[id].pos += x;
    int p = a[id].up;
    while (p) {
        a[p].pos += x;
        p = a[p].up;
    }
}
void Move2(int id, int x) {
    for (int i = 1; i <= 6; i++) {
        if (a[i].up == id) {
            a[i].up = a[id].up;
            a[id].up = 0;
        }
    }
    for (int i = 1; i <= 6; i++) {
        if (a[i].up == 0 && a[i].pos == a[id].pos + x) {
            a[i].up = id;
            break;
        }
    }
    a[id].pos += x;
}
bool Check1() {
    for (int i = 1; i <= 6; i++) {
        if (a[i].id == 1)continue;
        if (a[i].pos < a[1].pos)return false;
        if (a[i].up == 1)return false;
    }
    return true;
}
bool Check2() {
    return Random(100) <= 28;
}
bool Check3() {
    return Random(100) <= 65;
}
bool Check4() {
    return Random(100) <= 40;
}
bool Check5() {
    return Random(100) <= 50;
}
int Count(int p) {
    int res = 0;
    for (int i = 1; i <= 6; i++) {
        if (a[i].pos == p)res++;
    }
    return res;
}
void Work() {
    while (1) {
        for (int i = 1; i <= 6; i++) {
            int id = b[i], x = Random(3);
            if (id == 1 && Check1())x += 3;
            if (id == 2 && Check2())x *= 2;
            if (id == 5 && Check5()) {
                x += Count(a[i].pos) - 1;
                Move2(id, x);
                continue;
            }
            if (id == 6)x = Random(2) + 1;
            Move(id, x);
            if (a[id].pos >= 23) {
                int p = id;
                while (a[p].up)p = a[p].up;
                cnt[p]++;
                return;
            }
        }
        random_shuffle(b + 1, b + 6 + 1);
        if (Check3())while (b[6] != 3)random_shuffle(b + 1, b + 6 + 1);
        if (Check4()) {
            int x = 0;
            for (int i = 1; i <= 6; i++) {
                if (a[i].up == 4)x = i;
            }
            if (x)a[x].up = a[4].up;
            a[4].up = 0;
            for (int i = 1; i <= 6; i++) {
                if (i == 4)continue;
                if (a[i].up == 0 && a[i].pos == a[4].pos) {
                    a[i].up = 4;
                    break;
                }
            }
        }
    }
}
int main() {
    srand(time(NULL));
    int T = 1000000;
    for (int i = 1; i <= T; i++) {
        Init();
        Work();
    }
    cout << "T = " << T << endl;
    for (int i = 1; i <= 6; i++) {
        cout << a[i].name << " : " << 1.0 * cnt[i] / T * 100 << "%" << endl;
    }
    return 0;
}