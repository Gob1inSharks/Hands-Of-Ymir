using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MqttControlledBlock : MonoBehaviour
{
    int X_SCALE_FACTOR = 5;
    int Y_SCALE_FACTOR = 5;
    int Z_SCALE_FACTOR = 100;
    Vector3 fingerPosition = new Vector3(0f, 0f, 0f);
    Vector3 lastFingerPosition = new Vector3(0f, 0f, 0f);

    private Vector3 GetFingerPostion()
    {
        return new Vector3 (X_SCALE_FACTOR*Globals.m_Position[0], 
                            Y_SCALE_FACTOR*Globals.m_Position[1], 
                            Z_SCALE_FACTOR*Globals.m_Position[2]);
    }

    private void Start()
    {
        transform.position = fingerPosition;
    }

    private void Update()
    {
        fingerPosition = GetFingerPostion();
        if (fingerPosition != lastFingerPosition)
        {
            lastFingerPosition = fingerPosition;
            Debug.Log("Block Position Updated," + fingerPosition);
        }
        transform.position = fingerPosition;

    }
}