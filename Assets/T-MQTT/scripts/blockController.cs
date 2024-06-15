using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class blockController : mqttController
{

    Vector3 m_Movement;
    Rigidbody m_Rigidbody;

    void Start()
    {
        m_Rigidbody = GetComponent<Rigidbody>();
    }

    public override void OnMessageArrivedHandler(string newMsg)
    {
        {
        Debug.Log("MQTT Event Fired." +nameController+" message:" + newMsg);
        string[] Coordinates = newMsg.Split(new string[] { "," }, System.StringSplitOptions.None);
        m_Movement = new Vector3(float.Parse(Coordinates[0]), float.Parse(Coordinates[1]), float.Parse(Coordinates[2]));
        m_Rigidbody.MovePosition(m_Rigidbody.position + m_Movement * Time.deltaTime);
        }
    }
}