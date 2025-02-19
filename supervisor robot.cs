using UnityEngine;

public class RobotObserver : MonoBehaviour
{
    public Transform worker;
    public Transform target;

    void Update()
    {
        Debug.Log("Worker position: " + worker.position + " | Target position: " + target.position);
    }
}