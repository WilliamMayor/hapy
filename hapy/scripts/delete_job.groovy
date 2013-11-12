def delClos
delClos = { it.eachDir( delClos );
            it.eachFile {
                it.delete()
            }
        it.delete()
}
delClos( job.jobDir )