from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import CoolProp.CoolProp as CP
import numpy as np
import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
import traceback
import logging

class Resultados(APIView):
    
    def post(self, request,format=None):
        logger = logging.getLogger(__name__)
        try:
            
            
            pr = request.data.get('pr') #Ingresa como constante
            t_1_c = request.data.get('t_1') #Ingresa como Celcius pasar a Kelvin
            p_1_pa = request.data.get('p_1') #Ingresa como kiloPascal y trabaja en pascal
            q_ent = request.data.get('q_ent')#Ingresa como KJ/kg
            t_ent_c = request.data.get('t_ent')#Ingresa como Celcius pasar a Kelvin
            E_ent = request.data.get('E_ent') #Ingresa como KW
            if pr is None or t_1_c is None or p_1_pa is None or q_ent is None or t_ent_c is None or E_ent is None:
                return Response({"error": "Datos ingresados estan incorrectos o incompletos"}, status=status.HTTP_400_BAD_REQUEST)

            
            
            t_ent = t_ent_c + 273.15
            fluid = 'Air'
            k=1.4
            c_p = 1.006

            #ESTADO 1
            t_1 = t_1_c + 273.15
            p_1 = p_1_pa * 1000
            s_1 = round(CP.PropsSI('S','P',p_1,'T',t_1,fluid)/1000,3) #Entropia en kJ/kg.K
            h_1 = round(CP.PropsSI('H','P',p_1,'T',t_1,fluid)/1000,3) #Entalpia en kJ/kg
            d_1 = CP.PropsSI('D','T',t_1,'P',p_1,fluid) #Volumen especifico en m3/kg
            v_1 = round(1/d_1,3) #Volumen especifico en m3/kg

            #ESTADO 2
            p_2 =pr*p_1 #Presion 2 en Pa
            s_2 = s_1 #Entropia 2 en kJ/kg.K
            t_2 = t_1*(pr)**((k-1)/k) #Temperatura 2 en Kelvin
            h_2 = round(CP.PropsSI('H','P',p_2,'T',t_2,fluid)/1000,3) #Entalpia en kJ/kg
            d_2 = CP.PropsSI('D','T',t_2,'P',p_2,fluid) #Volumen especifico en m3/kg
            v_2 = round(1/d_2,3)

            #ESTADO 3
            t_3 = t_1 #Temperatura 3 en Kelvin
            h_3 = h_1 #Entalpia 3 en kJ/kg
            p_3 = p_2 #Presion 3 en Pa
            s_3 = round(CP.PropsSI('S','P',p_3,'T',t_3,fluid)/1000,3) #Entropia en kJ/kg.K
            d_3 = CP.PropsSI('D','T',t_3,'P',p_3,fluid) #Volumen especifico en m3/kg
            v_3 = round(1/d_3,3)

            #ESTADO 4
            t_4 = t_2 #Temperatura 4 en Kelvin
            h_4 = h_2 #Entalpia 4 en kJ/kg
            p_4 = pr*p_3 #Presion 4 en Pa
            s_4 = s_3 #Entropia 4 en kJ/kg.K
            d_4 = CP.PropsSI('D','T',t_4,'P',p_4,fluid) #Volumen especifico en m3/kg
            v_4 = round(1/d_4,3)

            #ESTADO 5
            t_5 = t_4 + t_ent #Temperatura 5 en Kelvin
            p_5 = p_4 #Presion 5 en Pa
            s_5 = round(CP.PropsSI('S','P',p_5,'T',t_5,fluid)/1000,3) #Entropia en kJ/kg.K
            h_5 = round(CP.PropsSI('H','P',p_5,'T',t_5,fluid)/1000,3) #Entalpia en kJ/kg
            d_5 = CP.PropsSI('D','T',t_5,'P',p_5,fluid) #Volumen especifico en m3/kg
            v_5 = round(1/d_5,3)

            #ESTADO 6
            p_6 =p_5 #Presion 6 en Pa
            t_6 =t_5 +(q_ent/c_p) #Temperatura 6 en Kelvin
            s_6 = round(CP.PropsSI('S','P',p_6,'T',t_6,fluid)/1000,3) #Entropia en kJ/kg.K
            h_6 = round(CP.PropsSI('H','P',p_6,'T',t_6,fluid)/1000,3) #Entalpia en kJ/kg
            d_6 = CP.PropsSI('D','T',t_6,'P',p_6,fluid) #Volumen especifico en m3/kg
            v_6 = round(1/d_6,3)

            #ESTADO 7
            p_7 = p_6/pr #Presion 7 en Pa
            t_7 = t_6/((pr)**((k-1)/k)) #Temperatura 7 en Kelvin
            s_7 = s_6 #Entropia en kJ/kg.K
            h_7 = round(CP.PropsSI('H','P',p_7,'T',t_7,fluid)/1000,3) #Entalpia en kJ/kg
            s_7_no = round(CP.PropsSI('S','P',p_7,'T',t_7,fluid)/1000,3) #Entropia en kJ/kg.K
            d_7 = CP.PropsSI('D','T',t_7,'P',p_7,fluid) #Volumen especifico en m3/kg
            v_7 = round(1/d_7,3)

            #ESTADO 8
            p_8 = p_7 #Presion 8 en Pa
            t_8 = t_7 +(q_ent/c_p) #Temperatura 8 en Kelvin
            s_8 = round(CP.PropsSI('S','P',p_8,'T',t_8,fluid)/1000,3) #Entropia en kJ/kg.K
            h_8 = round(CP.PropsSI('H','P',p_8,'T',t_8,fluid)/1000,3) #Entalpia en kJ/kg
            d_8 = CP.PropsSI('D','T',t_8,'P',p_8,fluid) #Volumen especifico en m3/kg
            v_8 = round(1/d_8,3)

            #ESTADO 9
            p_9 = p_8/pr #Presion 9 en Pa
            t_9 = t_8/((pr)**((k-1)/k)) #Temperatura 9 en Kelvin
            s_9=s_8 #Entropia 9 en kJ/kg.K
            h_9 = round(CP.PropsSI('H','P',p_9,'T',t_9,fluid)/1000,3) #Entalpia en kJ/kg
            s_9_no = round(CP.PropsSI('S','P',p_9,'T',t_9,fluid)/1000,3) #Entropia en kJ/kg.K
            d_9 = CP.PropsSI('D','T',t_9,'P',p_9,fluid) #Volumen especifico en m3/kg
            v_9 = round(1/d_9,3)

            #ESTADO 10
            p_10 = p_9 #Presion 10 en Pa
            t_10 = t_9 - t_ent #Temperatura 10 en Kelvin
            s_10 = round(CP.PropsSI('S','P',p_10,'T',t_10,fluid)/1000,3) #Entropia en kJ/kg.K
            h_10 = round(CP.PropsSI('H','P',p_10,'T',t_10,fluid)/1000,3) #Entalpia en kJ/kg
            d_10 = CP.PropsSI('D','T',t_10,'P',p_10,fluid) #Volumen especifico en m3/kg
            v_10 = round(1/d_10,3)

            #ESTADO 11
            p_11 = p_10 #Presion 11 en Pa
            t_11 = t_1 
            s_11 = round(CP.PropsSI('S','P',p_11,'T',t_11,fluid)/1000,3) #Entropia en kJ/kg.K
            h_11 = round(CP.PropsSI('H','P',p_11,'T',t_11,fluid)/1000,3) #Entalpia en kJ/kg
            d_11 = CP.PropsSI('D','T',t_11,'P',p_11,fluid) #Volumen especifico en m3/kg
            v_11 = round(1/d_11,3)

            q_in = round(q_ent*2,2)
            #--------GRAFICAS--------
            globals().update({
                'v_1': v_1, 'p_1': p_1,
                'v_2': v_2, 'p_2': p_2,
                'v_3': v_3, 'p_3': p_3,
                'v_4': v_4, 'p_4': p_4,
                'v_5': v_5, 'p_5': p_5,
                'v_6': v_6, 'p_6': p_6,
                'v_7': v_7, 'p_7': p_7,
                'v_8': v_8, 'p_8': p_8,
                'v_9': v_9, 'p_9': p_9,
                'v_10': v_10, 'p_10': p_10,
                'v_11': v_11, 'p_11': p_11
            })
            v_values =[]
            p_values =[]
            plt.figure(figsize=(10, 6))
            for i in range(1, 11):
              v = globals().get(f'v_{i}', None)
              p = globals().get(f'p_{i}', None)
              if v is not None and p is not None:
                  p = p / 1000  # Convertir a KPa
                  v_values.append(v)
                  p_values.append(p)
                  plt.scatter(v, p, color='k', marker='o')
                  plt.text(v, p, f' {i}', fontsize=12, verticalalignment='bottom', horizontalalignment='right')
              else:
                  print(f'Variable v_{i} o p_{i} no definida o es None')

            if v_values and p_values:
              v_values.append(v_values[0])
              p_values.append(p_values[0])

            plt.plot(v_values, p_values, marker='o', linestyle='-', color='r')
            plt.xlabel('Volumen específico (m^3/kg)')
            plt.ylabel('Presión (KPa)')
            plt.title('Diagrama P vs v')
            plt.grid(True)
            p_v = io.BytesIO()
            plt.savefig(p_v, format='png')
            p_v.seek(0)
            image_p_v = base64.b64encode(p_v.getvalue()).decode('utf-8')
            plt.close()

            #DIAGRAMA T vs s
            def isobaric_curve_by_entropy(p, s_start, s_end, steps=100):
                ss = np.linspace(s_start, s_end, steps)
                ts = [CP.PropsSI('T', 'S', s*1000, 'P', p, fluid) for s in ss]
                return ts, ss

            #PROCESO ISOBARICO
            ts, ss = isobaric_curve_by_entropy(p_4, s_4, s_6)
            plt.plot(ss, ts, linestyle='-', color='g')
            plt.plot([s_7, s_8], [t_7, t_8], linestyle='-', color='g', )
            ts, ss = isobaric_curve_by_entropy(p_2, s_2, s_3)
            plt.plot(ss, ts, linestyle='-', color='g')
            plt.plot([s_9, s_10], [t_9, t_10], linestyle='-', color='g', )
            ts, ss = isobaric_curve_by_entropy(p_10, s_10, s_1)
            plt.plot(ss, ts, linestyle='-', color='g', label='Procesos isobáricos')

            # Procesos isoentrópicos (líneas rectas)
            plt.plot([s_3, s_4], [t_3, t_4], linestyle='--', color='b', )
            plt.plot([s_6, s_7], [t_6, t_7], linestyle='--', color='b', )
            plt.plot([s_8, s_9], [t_8, t_9], linestyle='--', color='b', )
            plt.plot([s_1, s_2], [t_1, t_2], linestyle='--', color='b', label='Procesos isoentrópicos')
            globals().update({
                's_1': s_1, 't_1': t_1,
                's_2': s_2, 't_2': t_2,
                's_3': s_3, 't_3': t_3,
                's_4': s_4, 't_4': t_4,
                's_5': s_5, 't_5': t_5,
                's_6': s_6, 't_6': t_6,
                's_7': s_7, 't_7': t_7,
                's_8': s_8, 't_8': t_8,
                's_9': s_9, 't_9': t_9,
                's_10': s_10, 't_10': t_10,
                's_11': s_11, 't_11': t_11
            })
            # Añadir puntos y etiquetas
            for i in range(1, 12):
              s = globals().get(f's_{i}', None)
              t = globals().get(f't_{i}', None)
              
              if s is None or t is None:
                  continue
              
              plt.scatter(s, t, color='k', marker='o')
              plt.text(s, t, f' {i}', fontsize=12, verticalalignment='bottom', horizontalalignment='right')


            plt.xlabel('Entropía (kJ/kg.K)')
            plt.ylabel('Temperatura (K)')
            plt.title('Diagrama T vs s ')
            plt.grid(True)
            T_s = io.BytesIO()
            plt.savefig(T_s, format='png')
            p_v.seek(0)
            image_T_s = base64.b64encode(T_s.getvalue()).decode('utf-8')
            plt.close()

            #GRAFICA 3
            pr_values = np.arange(2, 10,1)
            ws_values = []
            n_values = []
            pot_values = []
            r_w_values = []
            for rr in pr_values:
                p_2_g1 =rr*p_1 #Presion 2 en Pa
                t_2_g1 = t_1*(rr)**((k-1)/k) #Temperatura 2 en Kelvin
                h_2_g1 = round(CP.PropsSI('H','P',p_2_g1,'T',t_2_g1,fluid)/1000,3) #Entalpia en kJ/kg

                p_3_g1 = p_2_g1 #Presion 3 en Pa
                p_4_g1 = rr*p_3_g1 #Presion 4 en Pa
                t_4_g1 = t_2_g1 #Temperatura 4 en Kelvin

                p_5_g1 = p_4_g1 #Presion 5 en Pa
                t_5_g1 = t_4_g1 + t_ent
                #ESTADO 6
                p_6_g1 =p_5_g1 #Presion 6 en Pa
                t_6_g1 =t_5_g1 +(q_ent/c_p) #Temperatura 6 en Kelvin
                h_6_g1 = round(CP.PropsSI('H','P',p_6_g1,'T',t_6_g1,fluid)/1000,3) #Entalpia en kJ/kg


                #ESTADO 7
                p_7_g1 = p_6_g1/rr #Presion 7 en Pa
                t_7_g1 = t_6_g1/((rr)**((k-1)/k)) #Temperatura 7 en Kelvin
                h_7_g1 = round(CP.PropsSI('H','P',p_7_g1,'T',t_7_g1,fluid)/1000,3) #Entalpia en kJ/kg


                #ESTADO 8
                p_8_g1 = p_7_g1 #Presion 8 en Pa
                t_8_g1 = t_7_g1 +(q_ent/c_p) #Temperatura 8 en Kelvin
                h_8_g1 = round(CP.PropsSI('H','P',p_8_g1,'T',t_8_g1,fluid)/1000,3) #Entalpia en kJ/kg


                #ESTADO 9
                p_9_g1 = p_8_g1/rr #Presion 9 en Pa
                t_9_g1 = t_8_g1/((rr)**((k-1)/k)) #Temperatura 9 en Kelvin
                h_9_g1 = round(CP.PropsSI('H','P',p_9_g1,'T',t_9_g1,fluid)/1000,3) #Entalpia en kJ/kg
      
                w_comp_g1 = h_1-h_2_g1
                w_turb_1_g1 = h_6_g1-h_7_g1
                w_turb_2_g1 = h_8_g1-h_9_g1
                w_neto_g1 = round(2*w_comp_g1 + w_turb_1_g1 + w_turb_2_g1,2)
                n_g1 = round(w_neto_g1/q_in,2) 
                pot_g1 = round(((E_ent*w_neto_g1)/q_ent)/1000,2)
                r_w_g1 = round((w_neto_g1)/(w_turb_1_g1 + w_turb_2_g1),2)

                n_values.append(n_g1)
                ws_values.append(w_turb_1_g1+w_turb_2_g1)
                pot_values.append(pot_g1)
                r_w_values.append(r_w_g1)


            plt.plot(pr_values,ws_values, marker='o', color='b')
            plt.xscale('log')
            plt.xlabel('Razón de presiones (pr)')
            plt.ylabel('Trabajo salida neto (kJ/kg)')
            plt.title('Salida de trabajo vs PR')
            plt.grid(True)
            W_pr = io.BytesIO()
            plt.savefig(W_pr, format='png')
            W_pr.seek(0)
            image_W_pr = base64.b64encode(W_pr.getvalue()).decode('utf-8')
            plt.close()

            plt.plot(pr_values, n_values, marker='o', color='b')
            plt.xscale('log')
            plt.xlabel('Razón de presiones (pr)')
            plt.ylabel('eficiencia (n)')
            plt.title('n vs PR')
            plt.grid(True)
            n_pr = io.BytesIO()
            plt.savefig(n_pr, format='png')
            n_pr.seek(0)
            image_n_pr = base64.b64encode(n_pr.getvalue()).decode('utf-8')
            plt.close()

            plt.plot(pr_values, pot_values, marker='o', color='b')
            plt.xscale('log')
            plt.xlabel('Razón de presiones (pr)')
            plt.ylabel('Potencia de Salida (MW)')
            plt.title('Potencia de salida vs PR')
            plt.grid(True)
            p_pr = io.BytesIO()
            plt.savefig(p_pr, format='png')
            p_pr.seek(0)
            image_p_pr = base64.b64encode(p_pr.getvalue()).decode('utf-8')
            plt.close()

            plt.plot(pr_values,r_w_values, 'o-', color='navy', label='Rendimiento de Trabajo')
            plt.xscale('log')
            plt.xlabel('Relación de Presión (PR)', fontsize=12)
            plt.ylabel('Razón de trabajo', fontsize=12)
            plt.title('Razón de trabajo vs Relación de Presión ', fontsize=14)
            plt.grid(True, which="both", ls="--", linewidth=0.5)
            rw_pr = io.BytesIO()
            plt.savefig(rw_pr, format='png')
            rw_pr.seek(0)
            image_rw_pr = base64.b64encode(rw_pr.getvalue()).decode('utf-8')
            plt.close()

            #DIAGRAMA H vs s
            states = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
            h_values = [h_1, h_2, h_3, h_4, h_5, h_6, h_7, h_8, h_9, h_10, h_11]
            s_values = [s_1, s_2, s_3, s_4, s_5, s_6, s_7, s_8, s_9, s_10, s_11]
            plt.figure(figsize=(10, 6))
            plt.plot(s_values, h_values, marker='o', linestyle='-', color='b')
            for i, state in enumerate(states):
                plt.text(s_values[i], h_values[i], f'{state}', fontsize=12, ha='right')
            plt.title('Diagrama h-s (Entalpía vs Entropía)')
            plt.xlabel('Entropía (s) [kJ/kg.K]')
            plt.ylabel('Entalpía (h) [kJ/kg]')
            plt.grid(True)
            h_s = io.BytesIO()
            plt.savefig(h_s, format='png')
            h_s.seek(0)
            image_h_s = base64.b64encode(h_s.getvalue()).decode('utf-8')
            plt.close()

            #------RESULTADOS------
            #TRABAJO NETO
            w_comp = round((h_1-h_2),2)
            w_turb_1 = round((h_6-h_7),2)
            w_turb_2 = round((h_8-h_9),2)
            w_neto = round(2*w_comp + w_turb_1 + w_turb_2,2) #Trabajo neto en KJ/kg



            #EFICIENCIA
            n = round(w_neto/q_in,2) #Eficiencia
            #POTENCIA DE SALIDA
            pot = round(((E_ent*w_neto)/q_ent)/1000,2)
            #RAZON DE TRABAJOS
            r_w = round((w_neto)/(w_turb_1 + w_turb_2),2)

            calculos = [
               {'p_1': p_1/1000, 't_1': round(t_1-273.15,2), 's_1': s_1, 'h_1': h_1, 'v_1': v_1},
               {'p_2': p_2/1000, 't_2': round(t_2-273.15,2), 's_2': s_2, 'h_2': h_2, 'v_2': v_2},
               {'p_3': p_3/1000, 't_3': round(t_3-273.15,2), 's_3': s_3, 'h_3': h_3, 'v_3': v_3},
               {'p_4': p_4/1000, 't_4': round(t_4-273.15,2), 's_4': s_4, 'h_4': h_4, 'v_4': v_4},
               {'p_5': p_5/1000, 't_5': round(t_5-273.15,2), 's_5': s_5, 'h_5': h_5, 'v_5': v_5},
               {'p_6': p_6/1000, 't_6': round(t_6-273.15,2), 's_6': s_6, 'h_6': h_6, 'v_6': v_6},
               {'p_7': p_7/1000, 't_7': round(t_7-273.15,2), 's_7': s_7, 'h_7': h_7, 'v_7': v_7},
               {'p_8': p_8/1000, 't_8': round(t_8-273.15,2), 's_8': s_8, 'h_8': h_8, 'v_8': v_8},
               {'p_9': p_9/1000, 't_9': round(t_9-273.15,2), 's_9': s_9, 'h_9': h_9, 'v_9': v_9},
               {'p_10': p_10/1000, 't_10':round(t_10-273.15,2), 's_10': s_10, 'h_10': h_10, 'v_10': v_10},
            ]

            return Response({
                "w_comp": w_comp,
                "w_turb_1": w_turb_1,
                "w_turb_2": w_turb_2,
                "w_neto": w_neto,
                "q_in": q_in,
                "n": n,
                "pot": pot,
                "r_w": r_w,
                "calculos": calculos,
                "image_p_v": image_p_v,
                "image_T_s": image_T_s,
                "image_W_pr": image_W_pr,
                "image_n_pr": image_n_pr,
                "image_h_s": image_h_s,
                "image_p_pr": image_p_pr,
                "image_rw_pr": image_rw_pr
            })
        except Exception as e:           
          logger.error("Error occurred: %s", traceback.format_exc())
          return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
