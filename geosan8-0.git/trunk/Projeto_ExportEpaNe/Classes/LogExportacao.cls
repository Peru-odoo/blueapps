VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "LogExportacao"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Private arquivoLog As String                        'nome do arquivo de log com todas as opera��es ao exportar para o Epanet

'Definie a localiza��o/diret�rio onde vai ficar o arquivo de log de exporta��o do EPANET
'
'
'
Private Function DefineLocalizacao()
    arquivoLog = "\Controles\ExportaEpanet" & DateValue(Now) & "  " & TimeValue(Now) & ".log"    'define o nome completo do arquivo de log do sistema, inclu�ndo a data e hora em que o mesmo ser� gerado pela primeira vez
    arquivoLog = Replace(arquivoLog, "/", "-")                      'troca caractere / especial que n�o � aceito como parte do nome do arquivo
    arquivoLog = Replace(arquivoLog, ":", "-")                      'troca caractere : especial que n�o � aceito como parte do nome do arquivo
    arquivoLog = App.Path & arquivoLog                              'adiciona a localiza��o do caminho onde o aplicativo est� instalado

End Function
'Abre o arquivo de log do sistema, se existir outro com o mesmo nome apaga
'
'
'
Function AbrePrimeiraVez()
    DefineLocalizacao
    Open arquivoLog For Output As #5                                'Inicia o log do sistema, abrindo o arquivo sem apagar o log anterior, mantendo sempre o hist�rico
    Fecha
End Function
'Abre o arquivo de log para continuar gravanto
'
'
'
Private Function AbreParaContinuarGravando()
    Open arquivoLog For Append As #5                                'Inicia o log do sistema, abrindo o arquivo sem apagar o log anterior, mantendo sempre o hist�rico
End Function
'Fecha o arquivo de log
'
'
'
Private Function Fecha()
    Close #5
End Function
'Grava texto no arquivo de log
'
'
'
Function GravaTexto(texto As String)
    AbreParaContinuarGravando
    Print #5, vbCrLf & texto                                        'Pula uma linha antes de iniciar a escrita
    Fecha
End Function
