Attribute VB_Name = "Module1"
Sub CopyCells()
    Dim ws As Worksheet
    Dim rng As Range
    Dim cell As Range
    Dim sheetsArray As Variant
    Dim newWs As Worksheet
    Dim splitStr As Variant
    sheetsArray = Array("Regular-L", "Regular-P", "IUP", "Multikampus")

    For Each ws In ThisWorkbook.Worksheets
        If Not IsError(Application.Match(ws.Name, sheetsArray, 0)) Then
            For Each rng In ws.Range("D:D,I:I,N:N")
                If Len(rng.Value) = 3 Then
                    ' Copy 'Template' sheet and rename it
                    ThisWorkbook.Sheets("Template").Copy After:=ThisWorkbook.Sheets(ThisWorkbook.Sheets.Count)
                    Set newWs = ActiveSheet
                    newWs.Name = rng.Value

                    ' Copy the found cell to C2 of new sheet
                    newWs.Range("C2").Value = rng.Value

                    ' Separate string by first "/" found
                    splitStr = Split(rng.Offset(1, 0).Value, "/", 2)
                    newWs.Range("C3").Value = splitStr(0)
                    If UBound(splitStr) > 0 Then newWs.Range("C4").Value = splitStr(1)

                    ' Copy contents from row 5 column 0 to row 19 column 2 twice to new sheet on C8 and C27
                    ws.Range(ws.Cells(rng.Row + 4, rng.Column - 1), ws.Cells(rng.Row + 18, rng.Column + 1)).Copy newWs.Range("C8")
                    ws.Range(ws.Cells(rng.Row + 4, rng.Column - 1), ws.Cells(rng.Row + 18, rng.Column + 1)).Copy newWs.Range("C27")
                End If
            Next rng
        End If
    Next ws
End Sub
