function Start-ProdEnv {
    docker-compose -f docker-compose.prod.yml up -d
}

function Stop-ProdEnv {
    docker-compose -f docker-compose.prod.yml down
}

function Get-ProdLogs {
    docker-compose -f docker-compose.prod.yml logs -f
}

# Export the functions
Export-ModuleMember -Function Start-ProdEnv, Stop-ProdEnv, Get-ProdLogs