Attribute VB_Name = "Module1"
Sub ClearCells()
    Dim ws As Worksheet
    Dim rng As Range
    Dim cell As Range
    Dim sheetsArray As Variant
    sheetsArray = Array("Regular-L", "Regular-P", "IUP", "Multikampus")

    For Each ws In ThisWorkbook.Worksheets
        If Not IsError(Application.Match(ws.Name, sheetsArray, 0)) Then
            For Each rng In ws.Range("D:D,I:I,N:N")
                If Len(rng.Value) = 3 Then
                    rng.Value = ""
                    rng.Offset(1, 0).Value = ""
                    rng.Offset(2, 0).Value = ""
                    ws.Range(ws.Cells(rng.Row + 4, rng.Column - 1), ws.Cells(rng.Row + 18, rng.Column + 1)).ClearContents
                End If
            Next rng
        End If
    Next ws
End Sub

