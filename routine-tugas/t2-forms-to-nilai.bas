Attribute VB_Name = "Module1"
Sub CreateManifest()
    Dim ws As Worksheet
    Dim destWs As Worksheet
    Dim destRow As Long

    ' Set the destination worksheet (change "Rekapitulasi" to the name of your sheet)
    Set destWs = ThisWorkbook.Sheets("Rekapitulasi")
    destRow = 2 ' Start copying to row 2

    ' Loop through each worksheet in the workbook
    For Each ws In ThisWorkbook.Sheets
        ' Skip the destination worksheet and the specified sheets
        If ws.Name <> destWs.Name And ws.Name <> "Rekapitulasi" And ws.Name <> "Template" And ws.Name <> "Mentor" Then
            ' Loop from row 8 to 22
            For i = 8 To 22
                ' If the cell in column B is not empty, copy columns B, C, and D to the destination worksheet
                If Not IsEmpty(ws.Cells(i, "B")) Then
                    ws.Range(ws.Cells(i, "B"), ws.Cells(i, "D")).Copy destWs.Cells(destRow, "B")
                    ' Add the name of the sheet to column E
                    destWs.Cells(destRow, "E").Value = ws.Name
                    ' Copy the value in column G to column F in the destination worksheet
                    destWs.Cells(destRow, "F").Value = ws.Cells(i, "G").Value
                    ' Copy the value in column E at row i+19 to column H in the destination worksheet
                    destWs.Cells(destRow, "H").Value = ws.Cells(i + 19, "E").Value
                    ' Move to the next row in the destination worksheet
                    destRow = destRow + 1
                End If
            Next i
        End If
    Next ws
End Sub


