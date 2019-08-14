#ifdef BACKEND_OPEN62541

#include <opcserver_open62541.h>

#include <LogIt.h>
#include <stdexcept>
#include <Utils.h>
#include <shutdown.h>

using namespace std;


#define throw_runtime_error_with_origin(MSG) throw std::runtime_error(std::string("At ")+__FILE__+":"+Utils::toString(__LINE__)+" "+MSG)

OpcServer::OpcServer():
    m_nodemanager(0),
    m_server(nullptr)
{
    //NOTE: UA_Server created later because it needs configuration (which is supplied later)
}

/** Destruction. */
OpcServer::~OpcServer()
{
}

int OpcServer::setServerConfig(const UaString& configurationFile, const UaString& applicationPath)
{
    LOG(Log::INF) << "Note: with open62541 backend, there isn't (yet) XML configuration loading. Assuming hardcoded server settings (endpoint's port, etc.)";
    // NOTE: some basid settings are configured in ctr init list
    // TODO: XML config reading
    // TODO: currently with 1.0 we don't create server config anymore
    return 0;
}

int OpcServer::addNodeManager(ASNodeManager* pNodeManager)
{
    if (!m_nodemanager)
        m_nodemanager = pNodeManager;
    else
        throw_runtime_error_with_origin("Sorry, only 1 NodeManager is supported.");
    return 0;
}

int OpcServer::createCertificate (
        const UaString& backendConfigFile,
        const UaString& appPath)
{
    LOG(Log::ERR) << "Sorry, certificate creation is not supported(yet) with open62541 backend.";
    return -1;
}

int OpcServer::start()
{
    m_server = UA_Server_new();
    if (!m_server)
        throw_runtime_error_with_origin("UA_Server_new failed");
    UA_ServerConfig* config = UA_Server_getConfig(m_server);
    UA_ServerConfig_setMinimal(config, 4841, nullptr);
    m_nodemanager->linkServer(m_server);
    m_nodemanager->afterStartUp();
    UA_StatusCode status = UA_Server_run_startup(m_server);
    if (status != UA_STATUSCODE_GOOD)
    {
        LOG(Log::ERR) << "UA_Server_run_startup returned not-good, server can't start. Error was:" << UaStatus(status).toString().toUtf8();
        return -1;
    }
    else
        LOG(Log::INF) << "UA_Server_run_startup returned: " << UaStatus(status).toString().toUtf8() << ", continuing.";
    m_open62541_server_thread = boost::thread ( &OpcServer::runThread, this );
    return 0;

}

int OpcServer::stop(OpcUa_Int32 secondsTillShutdown, const UaLocalizedText& shutdownReason)
{
    m_open62541_server_thread.join();
    delete m_nodemanager;
    m_nodemanager = 0;
    UA_Server_delete(m_server);
    m_server = 0;
    return 0;
}


void OpcServer::runThread()
{
    while (g_RunningFlag)
    {
        UA_Server_run_iterate(m_server, true);
    }
    UA_StatusCode status = UA_Server_run_shutdown(m_server);
    if (status != UA_STATUSCODE_GOOD)
    {
        LOG(Log::ERR) << "UA_Server_run_shutdown returned not-good. Error was:" << UaStatus(status).toString().toUtf8();
    }
    else
        LOG(Log::INF) << "UA_Server_run_shutdown returned: " << UaStatus(status).toString().toUtf8();
}

#endif //  BACKEND_OPEN62541
