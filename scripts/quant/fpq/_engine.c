// Motor diario de carteras con reglas. Compilar: gcc -O2 -shared -fPIC -o _engine.so _engine.c -lm
#include <math.h>
#include <stdlib.h>
#define MAXN 64
// stats: 0 nreb,1 nsw,2 ntrim,3 turnover,4 costes,5 impuestos,6 nband
void fpq_run(int T,int N,const double*R,const double*w,const double*up,const double*dn,const unsigned char*lev,const double*refw,
  const signed char*sig,const unsigned char*mlast,const int*mon,int every,int phase,int reset,const double*trim_at,const double*trim_to,
  const unsigned char*rec,double tc,double swc,const double*flow,int flow_mode,double tax,double*eq,double*val,double*W,double*st){
  double h[MAXN],s[MAXN],f[MAXN],bas[MAXN],sb=0,carry=0,V0=1.0,E=1.0,levw=0; int mode=sig[0],anchor=phase,i,j,t;
  for(i=0;i<7;i++)st[i]=0;
  for(j=0;j<N;j++){h[j]=w[j];s[j]=0;f[j]=0;bas[j]=w[j];if(lev[j])levw+=w[j];}
  if(mode==1){double P=0;for(j=0;j<N;j++)if(lev[j]){P+=h[j];f[j]=levw>0?w[j]/levw:0;h[j]=0;bas[j]=0;}for(j=0;j<N;j++)s[j]=P*refw[j];sb=P;}
  for(t=0;t<T;t++){
    double tot=0,S=0,cost=0,txb=0,trd=0;
    for(j=0;j<N;j++){double g=1.0+R[t*N+j];h[j]*=g;s[j]*=g;}
    for(j=0;j<N;j++)S+=s[j];
    if(sig[t]!=mode){
      if(sig[t]==1){double P=0,B=0;for(j=0;j<N;j++)if(lev[j]){P+=h[j];B+=bas[j];}
        for(j=0;j<N;j++)if(lev[j]){f[j]=P>0?h[j]/P:0;h[j]=0;bas[j]=0;}
        txb+=P-B;cost+=swc*P;for(j=0;j<N;j++)s[j]+=P*refw[j];sb=P;S+=P;trd+=P;}
      else{txb+=S-sb;cost+=swc*S;for(j=0;j<N;j++){if(lev[j]){h[j]=f[j]*S;bas[j]=h[j];}s[j]=0;}trd+=S;S=0;sb=0;}
      mode=sig[t];st[1]+=1;}
    for(j=0;j<N;j++)tot+=h[j];tot+=S;
    // recorte de satélites
    for(j=0;j<N;j++)if(trim_at[j]>0&&!(mode==1&&lev[j])&&h[j]/tot>=trim_at[j]){
      double ex=h[j]-trim_to[j]*tot,den=0;int k;txb+=ex*(1.0-bas[j]/h[j]);bas[j]*=(h[j]-ex)/h[j];h[j]-=ex;cost+=tc*2*ex;trd+=ex;
      for(k=0;k<N;k++)if(rec[j*N+k])den+=h[k];
      for(k=0;k<N;k++)if(rec[j*N+k]){double a=den>0?ex*h[k]/den:0;h[k]+=a;bas[k]+=a;}
      st[2]+=1;}
    // decisión de rebalanceo
    int doit=0,band=0;
    if(every>0&&mlast[t]&&((mon[t]-anchor)%every+every)%every==0)doit=1;
    for(j=0;j<N;j++){double nw=(mode==1&&lev[j])?f[j]*S/tot:h[j]/tot; if(w[j]>0||nw>0){if(nw>=up[j]||nw<=dn[j]){doit=1;band=1;}}}
    if(doit){double traded=0;
      for(j=0;j<N;j++){ if(mode==1&&lev[j])continue; double tg=tot*w[j],d=tg-h[j];
        if(d<0&&h[j]>0){txb+=(-d)*(1.0-bas[j]/h[j]);bas[j]*=tg/h[j];}else bas[j]+=d; traded+=fabs(d);h[j]=tg;}
      if(mode==1){double St=tot*levw,d=St-S; if(d<0&&S>0){txb+=(-d)*(1.0-sb/S);sb*=St/S;}else sb+=d; traded+=fabs(d);
        for(j=0;j<N;j++){s[j]=St*refw[j];if(lev[j]){f[j]=levw>0?w[j]/levw:0;h[j]=0;}}S=St;}
      cost+=tc*traded;trd+=traded/2;st[0]+=1;if(band){st[6]+=1;if(reset)anchor=mon[t];}}
    // costes e impuestos (con compensación de pérdidas)
    double due=0; if(tax>0){double net=txb+carry; if(net>0){due=tax*net;carry=0;}else carry=net;}
    st[3]+=trd/tot;st[4]+=cost/tot;st[5]+=due/tot;
    if(cost+due>0){double k=1.0-(cost+due)/tot;for(j=0;j<N;j++){h[j]*=k;s[j]*=k;bas[j]*=k;}sb*=k;S*=k;tot*=k;}
    E*=tot/V0; eq[t]=E; val[t]=tot;
    if(W)for(j=0;j<N;j++)W[t*N+j]=(h[j]+s[j])/tot;
    double a=flow?flow[t]:0;
    if(a!=0){ if(a<-0.999*tot)a=-0.999*tot;
      if(flow_mode==0){double k=1.0+a/tot;for(j=0;j<N;j++){h[j]*=k;s[j]*=k;bas[j]*=k;}sb*=k;}
      else{for(j=0;j<N;j++){if(mode==1&&lev[j]){int k2;for(k2=0;k2<N;k2++)s[k2]+=a*w[j]*refw[k2];sb+=a*w[j];}else{h[j]+=a*w[j];bas[j]+=a*w[j];}}}
      tot+=a;}
    V0=tot;
  }
}
