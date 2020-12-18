\ Model WordChain_TSP
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  var_arc[SGALWDV,GALWDVP] + 2 var_arc[SGALWDV,ALWDVPS]
   + 3 var_arc[SGALWDV,LWDVPSP] + 4 var_arc[SGALWDV,WDVPSPV]
   + 7 var_arc[S,SGALWDV] + var_arc[GALWDVP,ALWDVPS]
   + 2 var_arc[GALWDVP,LWDVPSP] + 3 var_arc[GALWDVP,WDVPSPV]
   + 7 var_arc[S,GALWDVP] + 6 var_arc[ALWDVPS,SGALWDV]
   + var_arc[ALWDVPS,LWDVPSP] + 2 var_arc[ALWDVPS,WDVPSPV]
   + 7 var_arc[S,ALWDVPS] + var_arc[LWDVPSP,WDVPSPV] + 7 var_arc[S,LWDVPSP]
   + 7 var_arc[S,WDVPSPV] + 0 var_seq[S]
Subject To
 R0: var_arc[SGALWDV,S] + var_arc[GALWDVP,S] + var_arc[ALWDVPS,S]
   + var_arc[LWDVPSP,S] + var_arc[WDVPSPV,S] = 1
 R1: var_arc[S,SGALWDV] + var_arc[ALWDVPS,SGALWDV] = 1
 R2: var_arc[SGALWDV,GALWDVP] + var_arc[S,GALWDVP] = 1
 R3: var_arc[SGALWDV,ALWDVPS] + var_arc[GALWDVP,ALWDVPS]
   + var_arc[S,ALWDVPS] = 1
 R4: var_arc[SGALWDV,LWDVPSP] + var_arc[GALWDVP,LWDVPSP]
   + var_arc[ALWDVPS,LWDVPSP] + var_arc[S,LWDVPSP] = 1
 R5: var_arc[SGALWDV,WDVPSPV] + var_arc[GALWDVP,WDVPSPV]
   + var_arc[ALWDVPS,WDVPSPV] + var_arc[LWDVPSP,WDVPSPV]
   + var_arc[S,WDVPSPV] = 1
 R6: var_arc[S,SGALWDV] + var_arc[S,GALWDVP] + var_arc[S,ALWDVPS]
   + var_arc[S,LWDVPSP] + var_arc[S,WDVPSPV] = 1
 R7: var_arc[SGALWDV,GALWDVP] + var_arc[SGALWDV,ALWDVPS]
   + var_arc[SGALWDV,LWDVPSP] + var_arc[SGALWDV,WDVPSPV]
   + var_arc[SGALWDV,S] = 1
 R8: var_arc[GALWDVP,ALWDVPS] + var_arc[GALWDVP,LWDVPSP]
   + var_arc[GALWDVP,WDVPSPV] + var_arc[GALWDVP,S] = 1
 R9: var_arc[ALWDVPS,SGALWDV] + var_arc[ALWDVPS,LWDVPSP]
   + var_arc[ALWDVPS,WDVPSPV] + var_arc[ALWDVPS,S] = 1
 R10: var_arc[LWDVPSP,WDVPSPV] + var_arc[LWDVPSP,S] = 1
 R11: var_arc[WDVPSPV,S] = 1
 R12: 6 var_arc[SGALWDV,GALWDVP] + var_seq[SGALWDV] - var_seq[GALWDVP]
   <= 5
 R13: 6 var_arc[SGALWDV,ALWDVPS] + var_seq[SGALWDV] - var_seq[ALWDVPS]
   <= 5
 R14: 6 var_arc[SGALWDV,LWDVPSP] + var_seq[SGALWDV] - var_seq[LWDVPSP]
   <= 5
 R15: 6 var_arc[SGALWDV,WDVPSPV] + var_seq[SGALWDV] - var_seq[WDVPSPV]
   <= 5
 R16: 6 var_arc[GALWDVP,ALWDVPS] + var_seq[GALWDVP] - var_seq[ALWDVPS]
   <= 5
 R17: 6 var_arc[GALWDVP,LWDVPSP] + var_seq[GALWDVP] - var_seq[LWDVPSP]
   <= 5
 R18: 6 var_arc[GALWDVP,WDVPSPV] + var_seq[GALWDVP] - var_seq[WDVPSPV]
   <= 5
 R19: 6 var_arc[ALWDVPS,SGALWDV] - var_seq[SGALWDV] + var_seq[ALWDVPS]
   <= 5
 R20: 6 var_arc[ALWDVPS,LWDVPSP] + var_seq[ALWDVPS] - var_seq[LWDVPSP]
   <= 5
 R21: 6 var_arc[ALWDVPS,WDVPSPV] + var_seq[ALWDVPS] - var_seq[WDVPSPV]
   <= 5
 R22: 6 var_arc[LWDVPSP,WDVPSPV] + var_seq[LWDVPSP] - var_seq[WDVPSPV]
   <= 5
Bounds
Binaries
 var_arc[SGALWDV,GALWDVP] var_arc[SGALWDV,ALWDVPS] var_arc[SGALWDV,LWDVPSP]
 var_arc[SGALWDV,WDVPSPV] var_arc[S,SGALWDV] var_arc[SGALWDV,S]
 var_arc[GALWDVP,ALWDVPS] var_arc[GALWDVP,LWDVPSP] var_arc[GALWDVP,WDVPSPV]
 var_arc[S,GALWDVP] var_arc[GALWDVP,S] var_arc[ALWDVPS,SGALWDV]
 var_arc[ALWDVPS,LWDVPSP] var_arc[ALWDVPS,WDVPSPV] var_arc[S,ALWDVPS]
 var_arc[ALWDVPS,S] var_arc[LWDVPSP,WDVPSPV] var_arc[S,LWDVPSP]
 var_arc[LWDVPSP,S] var_arc[S,WDVPSPV] var_arc[WDVPSPV,S]
Generals
 var_seq[S] var_seq[SGALWDV] var_seq[GALWDVP] var_seq[ALWDVPS]
 var_seq[LWDVPSP] var_seq[WDVPSPV]
End
