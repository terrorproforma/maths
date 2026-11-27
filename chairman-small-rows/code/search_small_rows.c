// general m offline: maximise over instances the min over assignments of max row-prefix |disc|, D=1
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#define NMAX 24
#define MMAX 6
int n,m; double Dw[NMAX][MMAX],X[NMAX][MMAX]; double best;
static void rec(int j,double*s,double cur){
  if(cur>=best) return;
  if(j==n){best=cur;return;}
  double base[MMAX],c[MMAX];int ord[MMAX];
  for(int i=0;i<m;i++)base[i]=s[i]+Dw[j][i]*X[j][i];
  double mx1=0,mx2=0;int arg=-1; // max |base| and second
  for(int i=0;i<m;i++){double v=fabs(base[i]);if(v>mx1){mx2=mx1;mx1=v;arg=i;}else if(v>mx2)mx2=v;}
  for(int i=0;i<m;i++){double o=(i==arg)?mx2:mx1;c[i]=fmax(o,fabs(base[i]-Dw[j][i]));ord[i]=i;}
  for(int a=0;a<m;a++)for(int b=a+1;b<m;b++)if(c[ord[b]]<c[ord[a]]){int t=ord[a];ord[a]=ord[b];ord[b]=t;}
  for(int k=0;k<m;k++){int i=ord[k];double nc=fmax(cur,c[i]);if(nc>=best)break;
    double t[MMAX];memcpy(t,base,sizeof(double)*m);t[i]-=Dw[j][i];rec(j+1,t,nc);}
}
double eval(){best=1e9;double s[MMAX]={0};rec(0,s,0);return best;}
double rnd(){return rand()/(RAND_MAX+1.0);}
double clip(double x){return x<0?0:(x>1?1:x);}
void norm(int j){double t=0;for(int i=0;i<m;i++)t+=X[j][i];if(t<1e-9){for(int i=0;i<m;i++)X[j][i]=1.0/m;}else for(int i=0;i<m;i++)X[j][i]/=t;}
int main(int argc,char**argv){
  m=atoi(argv[1]);n=atoi(argv[2]);srand(atoi(argv[3]));long iters=atol(argv[4]);
  double gb=0;
  for(;;){
    for(int j=0;j<n;j++){for(int i=0;i<m;i++){Dw[j][i]=rnd()<0.4?(rnd()<0.4?0:1):rnd();X[j][i]=rnd()<0.3?0:rnd();}norm(j);}
    double v=eval(),T=0.02;
    for(long it=0;it<iters;it++){
      int j=rand()%n,i=rand()%m;double od[MMAX],ox[MMAX];memcpy(od,Dw[j],sizeof od);memcpy(ox,X[j],sizeof ox);
      double r=rnd();
      if(r<0.45){double q=rnd();Dw[j][i]=q<0.1?rnd():(q<0.25?(rnd()<0.5?0:1):clip(od[i]+(rnd()-0.5)*(q<0.6?0.2:0.02)));}
      else if(r<0.9){double q=rnd();X[j][i]=q<0.1?rnd():(q<0.2?0:clip(ox[i]+(rnd()-0.5)*(q<0.6?0.2:0.02)));norm(j);}
      else{int j2=rand()%n;double td[MMAX],tx[MMAX];memcpy(td,Dw[j2],sizeof td);memcpy(tx,X[j2],sizeof tx);
           memcpy(Dw[j2],Dw[j],sizeof td);memcpy(X[j2],X[j],sizeof tx);memcpy(Dw[j],td,sizeof td);memcpy(X[j],tx,sizeof tx);
           double v2=eval();if(v2>=v||rnd()<exp((v2-v)/T))v=v2;else{memcpy(Dw[j],Dw[j2],sizeof td);memcpy(X[j],X[j2],sizeof tx);memcpy(Dw[j2],td,sizeof td);memcpy(X[j2],tx,sizeof tx);}
           T*=0.9997;continue;}
      double v2=eval();
      if(v2>=v||rnd()<exp((v2-v)/T)){v=v2;}else{memcpy(Dw[j],od,sizeof od);memcpy(X[j],ox,sizeof ox);}
      T*=0.9997;
    }
    if(v>gb){gb=v;printf("m=%d n=%d val=%.6f\n",m,n,v);for(int j=0;j<n;j++){printf(" d:");for(int i=0;i<m;i++)printf(" %.4f",Dw[j][i]);printf("  x:");for(int i=0;i<m;i++)printf(" %.4f",X[j][i]);printf("\n");}fflush(stdout);}
  }
}
