
"""
# -- ---------------------------------------------------------------------------------------------------------      -- #
# -- project: Lab 3 (Behavioral Finance) is a project that has tools to analyze the performance of trade history.   -- #
# -- script: functions.py : Python script with the main functionality                                               -- #
# -- author: EstebanMqz                                                                                             -- #
# -- license: GNU General Public License v3.0                                                                       -- #
# -- repository: https://github.com/EstebanMqz/MyST_LAB_3_E3                                                        -- #
# -- ---------------------------------------------------------------------------------------------------------      -- #
"""

from dataclasses import dataclass
import pandas as pd
import pandas_datareader as pdr
from lib2to3.pgen2.grammar import opmap_raw
import numpy as np
from data import *

def f_leer_archivo(param_archivo):
    """
    Function that reads csv files and returns a dataframe of its content.

        Parameters
        ----------
        param_archivo: csv data.
        Returns
        -------
        data: pd.DataFrame(param_archivo)
    """

    df = pd.read_csv(param_archivo)
    return df


def symbols(param_sym):
        """
        A function to get unique values of the traded symbols in historical data and return
        its globally accepted denomination. Only Applicable to currencies.

        Parameters
        ----------
        param_sym: Instrument Symbols Column (Str) 
        ej: data.Símbolo
        -------
        Returns
        -------
        Symbols : Searchable traded symbols from historical data [List].      
        """
        symbols=param_sym.unique()
        symbols=[symbols[i][:3] + '_' + symbols[i][3:] for i in range(3)] #Applicable to currencies
        return symbols


def f_pip_size(param_ins, param_pips):
        """
        A function to get the multiplier number to express the price difference in pips.
        Mult = 100 for instruments denominated in monetary units.

        Parameters
        ----------
        param_ins: Instrument name to be associated with the corresponding pip multiplier (Str).
        param_pips: Instruments_pips values provided in the general tick size csv.
        -------
        Returns
        -------
        Pip Size : Int.      
        """

        Instr=param_pips[param_pips['Instrument'] == param_ins]
        pip_size=1/Instr['TickSize']
        return pip_size


def f_columnas_tiempos(param_data,Open,Close):
        """
        Function that calculates column Open_pos for the existing dataframe.
        Open_Pos: Calculates the difference between Open and Close time columns.

        Parameters
        ----------
        Open: Column of Open date as datetime64 format. 
        ej. data.Fecha/Hora for columns in files/Historics.csv
        Close: Column of Close date as datetime64 format. 
        ej. data.Fecha/Hora.1 for columns in files/Historics.csv
        -------
        returns: Time elapsed for an Open Position in seconds.
        + Open_Pos: A new column as datetime64 column, that represents the seconds for which the trade was open.
        """
        param_data['Open'] = pd.to_datetime(Open)
        param_data['Close'] = pd.to_datetime(Close)
        param_data['Open_Pos'] = pd.to_datetime(Close)-pd.to_datetime(Open)
        param_data['Open_Pos'] = param_data['Open_Pos'].dt.total_seconds()

        return param_data


def f_columnas_pips(param_data, pips):
        """
        Function that adds more columns of pip transformations.
        + Pips: Column where the number of resulting pips for each operation should be, including its sign:
        - Buy Trade: (closeprice - openprice)*mult.
        - Sell Trade: (openprice - closeprice)*mult.
        + pips_acm: The accumulated value of the pips column.
        + profit_acm: The accumulated value of the profit column.

        Parameters
        ----------
        param_data: DataFrame base.
        pips: General tick size file instruments.csv
        -------
        returns: Historic data with Pips, pips_acm, profit_acm new columns.
        """
        trades = []
        for i in range(len(param_data)):
                trades.append(f_pip_size(param_data.loc[i,'Símbolo'], pips))
        pips = pd.DataFrame(trades, columns=['Pips'])
        param_data["Pips"] = np.where(param_data['Tipo'] == "buy", 
        param_data["Precio.1"] - param_data["Precio"], 
        param_data["Precio"] - param_data["Precio.1"])
        param_data['pips_acm'] = param_data["Pips"].cumsum()
        param_data['Beneficio']=pd.to_numeric(param_data['Beneficio'].replace('-',np.nan)) 
        param_data['profit_acm'] = param_data["Beneficio"].cumsum()
        
        return param_data

def f_estadisticas_ba(param_data):
        """
        Function that makes a dataframe of general statistics expressed in rows and described in columns.

        Parameters
        ----------
        param_data: DataFrame base.
        -------
        returns: Dataframe with metrics rows and calculated. Rows integrated in historic trades dataframe as cols.
        + [Ops totales, Ops Ganadoras, Ops Perdedoras, "Ops Ganadoras_C, Ops Perdedoras_C, Ops Ganadoras_V, 
        Ops Perdedoras_V, Median, r_efectividad, r_proporcion, r_efectividad_c, r_efectividad_v]
        """
        metrics = ["Ops totales","Ganadoras","Ganadoras_c","Ganadoras_v","Perdedoras","Perdedoras_c","Perdedoras_v",
               "Mediana (Profit)","Mediana (Pips)","r_efectividad","r_proporcion","r_efectividad_c","r_efectividad_v"]
    
        description = ["Operaciones totales","Operaciones ganadoras","Operaciones ganadoras de compra",
               "Operaciones perdedoras de venta","Operaciones perdedoras","Operaciones perdedoras de compra",
               "Operaciones perdedoras de venta","Mediana de profit de operaciones",
               "Mediana de pips de operaciones","Ganadoras Totales/Operaciones Totales",
               "Ganadoras Totales/Perdedoras Totales","Ganadoras Compras/Operaciones Totales",
               "Ganadoras Ventas/ Operaciones Totales"]
    
        valor = np.zeros(13)
    
        datos_df1 = {"medidas":metrics,"valor":valor,"description":description}
        df_1_tabla = pd.DataFrame(datos_df1)

        param_data["Ops Totales"] = np.ones(len(param_data["Beneficio"]))
        param_data["Ops Ganadoras"] = np.zeros(len(param_data["Tipo"]))
        param_data["Ops Perdedoras"] = np.zeros(len(param_data["Tipo"]))
        param_data["Ops Ganadoras_C"] = np.zeros(len(param_data["Tipo"]))
        param_data["Ops Perdedoras_C"] = np.zeros(len(param_data["Tipo"]))
        param_data["Ops Ganadoras_V"] = np.zeros(len(param_data["Tipo"]))
        param_data["Ops Perdedoras_V"] = np.zeros(len(param_data["Tipo"]))
    
        df_1_tabla.valor[0] = len(param_data.Tipo)
    
        for i in range(len(param_data["Beneficio"])):
            if param_data["Beneficio"][i] > 0:
                param_data["Ops Ganadoras"][i] = 1
                param_data["Ops Perdedoras"][i] = 0
            else:
                param_data["Ops Ganadoras"][i] = 0
                param_data["Ops Perdedoras"][i] = 1
    
        df_1_tabla.valor[1] = sum(param_data["Ops Ganadoras"])
        df_1_tabla.valor[4] = sum(param_data["Ops Perdedoras"])
    
        for i in range(len(param_data["Beneficio"])):
            if param_data["Ops Ganadoras"][i] == 1 and param_data["Tipo"][i] == "buy" :
                param_data["Ops Ganadoras_C"][i] = 1
            elif param_data["Ops Ganadoras"][i] == 1 and param_data["Tipo"][i] == "sell" :
                param_data["Ops Ganadoras_V"][i] = 1
            elif param_data["Ops Perdedoras"][i] == 1 and param_data["Tipo"][i] == "buy" :
                param_data["Ops Perdedoras_C"][i] = 1
            elif param_data["Ops Perdedoras"][i] == 1 and param_data["Tipo"][i] == "sell" :
                param_data["Ops Perdedoras_V"][i] = 1
            else:
                param_data["Ops Ganadoras_C"][i] = 0
                param_data["Ops Ganadoras_V"][i] = 0
                param_data["Ops Perdedoras_C"][i] = 0
                param_data["Ops Perdedoras_V"][i] = 0
            
        df_1_tabla.valor[2] = sum(param_data["Ops Ganadoras_C"])
        df_1_tabla.valor[3] = sum(param_data["Ops Ganadoras_V"])
        df_1_tabla.valor[5] = sum(param_data["Ops Perdedoras_C"])
        df_1_tabla.valor[6] = sum(param_data["Ops Perdedoras_V"])
        
        df_1_tabla.valor[7] = param_data["Beneficio"].median()
        df_1_tabla.valor[8] = param_data["Pips"].median()
        
        df_1_tabla.valor[9] = round(sum(param_data["Ops Ganadoras"])/len(param_data["Ops Perdedoras"]),3)
        df_1_tabla.valor[10] = round(sum(param_data["Ops Ganadoras"])/sum(param_data["Ops Ganadoras"]),3)
        df_1_tabla.valor[11] = round(sum(param_data["Ops Ganadoras_C"])/len(param_data["Ops Ganadoras"]),3)
        df_1_tabla.valor[12] = round(sum(param_data["Ops Ganadoras_V"])/len(param_data["Ops Ganadoras"]),3)
        
        return df_1_tabla

def f_estadisticas_ba2(param_data):
        """
        Function that makes a dataframe with sorted ranking as percentage for the winning trade operations.

        Parameters
        ----------
        param_data: DataFrame base.
        -------
        returns: Dataframe with ranking of trade results.
        """   
        for i in range(len(param_data)):
            if param_data["Beneficio"][i] > 0:
                param_data["Ops Ganadoras"][i] = 1
                param_data["Ops Perdedoras"][i] = 0
            else:
                param_data["Ops Ganadoras"][i] = 0
                param_data["Ops Perdedoras"][i] = 1

        for i in range(len(param_data["Beneficio"])):
            if param_data["Ops Ganadoras"][i] == 1 and param_data["Tipo"][i] == "buy" :
                param_data["Ops Ganadoras_C"][i] = 1
            elif param_data["Ops Ganadoras"][i] == 1 and param_data["Tipo"][i] == "sell" :
                param_data["Ops Ganadoras_V"][i] = 1
            elif param_data["Ops Perdedoras"][i] == 1 and param_data["Tipo"][i] == "buy" :
                param_data["Ops Perdedoras_C"][i] = 1
            elif param_data["Ops Perdedoras"][i] == 1 and param_data["Tipo"][i] == "sell" :
                param_data["Ops Perdedoras_V"][i] = 1
            else:
                param_data["Ops Ganadoras_C"][i] = 0
                param_data["Ops Ganadoras_V"][i] = 0
                param_data["Ops Perdedoras_C"][i] = 0
                param_data["Ops Perdedoras_V"][i] = 0
                
            df_2_ranking = pd.pivot_table(param_data,index=["Símbolo"],aggfunc={"Ops Ganadoras":np.sum,"Ops Totales":np.sum})
            df_2_ranking["rank"] = (df_2_ranking["Ops Ganadoras"]/df_2_ranking["Ops Totales"])
            df_2_ranking = df_2_ranking.drop(["Ops Ganadoras","Ops Totales"],axis=1)
            df_2_ranking = df_2_ranking.sort_values('rank',ascending=False)
            df_2_ranking["rank"] = round(df_2_ranking["rank"],2)
            df_2_ranking["rank %"] = df_2_ranking["rank"].map(lambda x:format(x,'.2%'))
            #pivot_ord["rank"] = pivot_ord["rank"].map(lambda x:format(x,'.2%'))
            return df_2_ranking


def f_evolucion_capital(param_data):
        """
        Function that groups same day trades in rows in order to calculate the daily accumulated profit 
        and portfolio net value by daily timestamps.

        Parameters
        ----------
        param_data: DataFrame base.
        -------
        returns: Dataframe with cols:
        timestamp: On a daily basis.
        profit_d: Daily profit.
        profit_acum_d: Acum. daily profit.
        """

        param_data["day"] = param_data["Close"].dt.strftime("%Y-%m-%d")

        pivot2 = pd.pivot_table(param_data,index=["day"],aggfunc={"Beneficio":np.sum})

        pivot2["timestamp"] = pivot2.index.get_level_values("day")
        pivot2 = pivot2.reindex(columns=['timestamp', 'Beneficio'])
        
        start = datetime.strptime(param_data["day"].min(), "%Y-%m-%d")
        end = datetime.strptime(param_data["day"].max(), "%Y-%m-%d")
        date_generated = pd.date_range(start, end)
        date_generated = date_generated.strftime("%Y-%m-%d")
        
        d3 = {"timestamp":date_generated,"profit_d": np.zeros(len(date_generated))}
        registros_d = pd.DataFrame(d3)
        
        for i in range(len(registros_d["timestamp"])):
            for j in range(len(pivot2["timestamp"])):
                if registros_d["timestamp"][i] == pivot2["timestamp"][j]:
                    registros_d["profit_d"][i] = pivot2["Beneficio"][j]
                    
        registros_d["profit_acum_d"] = np.zeros(len(registros_d["profit_d"]))
        registros_d["profit_acum_d"][0] = 10000+registros_d["profit_d"][0]

        for i in range(1,len(registros_d["profit_d"])):
            registros_d["profit_acum_d"][i] = registros_d["profit_acum_d"][i-1]+registros_d["profit_d"][i]
            
        return registros_d


def f_estadisticas_mad(param_d_p,param_data):
        """
        Function that makes a dataframe of Performance Attribution Metrics expressed in rows and described in columns.

        Parameters
        ----------
        param_d_p: Daily portfolio behavior as dataframe from f_evolucion_capital function.
        param_data: DataFrame base.
        -------
        returns: Dataframe with metrics rows and calculated. Rows integrated in historic trades dataframe as cols.
        + ["sharpe_original","sharpe_actualizado","drawdown_capi","drawdown_capi","drawdown_capi" 
        Ops Perdedoras_V, Median, r_efectividad, r_proporcion, r_efectividad_c, r_efectividad_v]
        """
    
        # Sharpe Ratio Original
        param_d_p["rends_log"] = np.log(param_d_p["profit_acum_d"].shift(periods=1)/param_d_p["profit_acum_d"])
        param_d_p["rends_log"] = param_d_p["rends_log"]*-1
        param_d_p["rends_log"][0] = np.log(param_d_p["profit_acum_d"][0]/10000)
        rp = param_d_p["rends_log"].mean()
        std = param_d_p["rends_log"].std()
        #https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202210
        rf = 0.0330 #Mo 
        SRO = (rp-rf)/std
        
        # Sharpe Ratio Benchmark
        data_sp500 = pdr.DataReader("^GSPC", 'yahoo',datetime(2021,1,1),datetime(2022,10,14))["Adj Close"]
        data_sp500["Rends_log"] = np.log(data_sp500.shift(periods=1)/data_sp500)
        data_sp500["Rends_log"] = data_sp500["Rends_log"]*-1
        r_trader = rp
        r_benchmark = data_sp500["Rends_log"].mean()
        SRA = ((r_trader-r_benchmark)-rf)/std
        
        # Drawdown(Capital)
        param_data["Capital"] = np.zeros(len(param_data["profit_acm"]))
        param_data["Capital"][0] = 10000+param_data["profit_acm"][0]
        for i in range(1,len(param_data["profit_acm"])):
            param_data["Capital"][i] = param_data["Capital"][i-1]+param_data["Beneficio"][i]
        DDC_range = param_data[param_data['Capital'] == param_data["Capital"].min()]
        DDC = DDC_range.iloc[0,28]
        DDC_ot = DDC_range.iloc[0,14]
        DDC_ct = DDC_range.iloc[0,15]
        
        # Drawup(Capital)
        DUC_range = param_data[param_data['Capital'] == param_data["Capital"].max()]
        DUC = DUC_range.iloc[0,28]
        DUC_ot = DUC_range.iloc[0,14]
        DUC_ct = DUC_range.iloc[0,15]
        
        datos_desempeño = {"Metrica":["sharpe_original","sharpe_actualizado","drawdown_capi","drawdown_capi","drawdown_capi",
                                    "drawup_capi","drawup_capi","drawup_capi"],
                        "Tipo de Dato":["Cantidad","Cantidad","Fecha Inicial","Fecha Final","DrawDown $ (capital)","Fecha Inicial",
                                        "Fecha Final","DrawUp $ (capital)"],
                        "Valor":np.zeros(8),
                        "Descripcion":["Sharpe Ratio Fórmula Original","Sharpe Ratio Fórmula Ajustada","Fecha inicial del DrawDown de Capital",
                                        "Fecha final del DrawDown de Capital","Máxima pérdida flotante registrada",
                                        "Fecha inicial del DrawUp de Capital","Fecha final del DrawUp de Capital",
                                        "Máxima ganancia flotante registrada"]}
        
        tabla_desempeño = pd.DataFrame(datos_desempeño)
        
        tabla_desempeño["Valor"][0] = SRO
        tabla_desempeño["Valor"][1] = SRA
        tabla_desempeño["Valor"][4] = DDC
        tabla_desempeño["Valor"][2] = DDC_ot
        tabla_desempeño["Valor"][3] = DDC_ct
        tabla_desempeño["Valor"][7] = DUC
        tabla_desempeño["Valor"][5] = DUC_ot
        tabla_desempeño["Valor"][6] = DUC_ct

        return tabla_desempeño

